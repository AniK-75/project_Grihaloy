import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
from .models import Negotiation, Message

User = get_user_model()


class NegotiationConsumer(WebsocketConsumer):
    def connect(self):
        self.negotiation_pk = self.scope["url_route"]["kwargs"]["negotiation_pk"]
        self.negotiation_group_name = f"negotiation_{self.negotiation_pk}"
        self.user = self.scope["user"]

        # --- DIAGNOSTIC PRINT 1 ---
        print(f"CONNECT: User {self.user} connecting to group {self.negotiation_group_name}")

        # Check if user is authenticated and part of the negotiation
        if not self.user.is_authenticated:
            self.close()
            return

        try:
            self.negotiation = Negotiation.objects.get(pk=self.negotiation_pk)
            if self.user not in [self.negotiation.renter, self.negotiation.landlord]:
                print(f"CONNECT: User {self.user} is not part of this negotiation. Closing.")
                self.close()
                return
        except Negotiation.DoesNotExist:
            print("CONNECT: Negotiation does not exist. Closing.")
            self.close()
            return

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.negotiation_group_name, self.channel_name
        )
        self.accept()

        # --- DIAGNOSTIC PRINT 2 ---
        print(f"CONNECT: User {self.user} ACCEPTED and ADDED to group.")

    def disconnect(self, close_code):
        # --- DIAGNOSTIC PRINT 3 ---
        print(f"DISCONNECT: User {self.user} disconnecting from group {self.negotiation_group_name}")

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.negotiation_group_name, self.channel_name
        )

    # --- START MODIFIED RECEIVE METHOD ---
    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            command = text_data_json.get("command", "new_message")

            # --- DIAGNOSTIC PRINT 4 ---
            print(f"RECEIVE: User {self.user} sent command '{command}' with data: {text_data}")

            if command == "new_message":
                self.handle_new_message(text_data_json)
            elif command == "edit_message":
                self.handle_edit_message(text_data_json)
            elif command == "delete_message":
                self.handle_delete_message(text_data_json)

        except json.JSONDecodeError:
            print("ERROR: Invalid JSON received.")
        except Exception as e:
            print(f"Error processing message: {e}")
            self.send(text_data=json.dumps({
                'error': f'An internal error occurred: {e}'
            }))

    # --- NEW: Handles sending a new message ---
    def handle_new_message(self, data):
        message_content = data["message"]
        sender_id = data["sender_id"]  # Passed from frontend

        # Double check sender matches authenticated user
        if str(self.user.pk) != sender_id:
            self.send(text_data=json.dumps({'error': 'User authentication mismatch.'}))
            return

        # Save message to database
        message_obj = Message.objects.create(
            negotiation=self.negotiation,
            sender=self.user,
            content=message_content
        )
        print(f"NEW_MSG: Message from {self.user.username} saved to DB.")

        # Update negotiation timestamp and seen status
        self.negotiation.updated_at = timezone.now()
        if self.user == self.negotiation.renter:
            self.negotiation.seen_by_landlord = False
            self.negotiation.seen_by_renter = True
        else:  # sender is landlord
            self.negotiation.seen_by_renter = False
            self.negotiation.seen_by_landlord = True
        self.negotiation.save(update_fields=['updated_at', 'seen_by_landlord', 'seen_by_renter'])

        timestamp_str = message_obj.timestamp.strftime("%b %d, %H:%M")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.negotiation_group_name,
            {
                "type": "chat_message",
                "command": "new_message",
                "message_id": str(message_obj.pk),
                "message": message_obj.content,
                "sender_id": str(message_obj.sender.pk),
                "sender_name": message_obj.sender.username,
                "timestamp": timestamp_str,
                "is_edited": False,
            }
        )

    # --- NEW: Handles editing a message ---
    def handle_edit_message(self, data):
        message_id = data["message_id"]
        new_content = data["new_content"]

        try:
            message_obj = Message.objects.get(pk=message_id)

            # Security check: Only sender can edit
            if message_obj.sender != self.user:
                self.send(text_data=json.dumps({'error': 'You cannot edit this message.'}))
                return

            # Security check: Can't edit deleted messages
            if message_obj.is_deleted:
                self.send(text_data=json.dumps({'error': 'Cannot edit a deleted message.'}))
                return

            message_obj.content = new_content
            message_obj.is_edited = True
            message_obj.save(update_fields=['content', 'is_edited', 'updated_at'])

            print(f"EDIT_MSG: Message {message_id} edited by {self.user.username}.")

            timestamp_str = message_obj.updated_at.strftime("%b %d, %H:%M")

            async_to_sync(self.channel_layer.group_send)(
                self.negotiation_group_name,
                {
                    "type": "message_edited",
                    "command": "edit_message",
                    "message_id": str(message_obj.pk),
                    "new_content": message_obj.content,
                    "timestamp": timestamp_str,
                }
            )
        except Message.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Message not found.'}))

    # --- NEW: Handles deleting a message ---
    def handle_delete_message(self, data):
        message_id = data["message_id"]

        try:
            message_obj = Message.objects.get(pk=message_id)

            # Security check: Only sender can delete
            if message_obj.sender != self.user:
                self.send(text_data=json.dumps({'error': 'You cannot delete this message.'}))
                return

            message_obj.is_deleted = True
            message_obj.save(update_fields=['is_deleted'])

            print(f"DELETE_MSG: Message {message_id} deleted by {self.user.username}.")

            async_to_sync(self.channel_layer.group_send)(
                self.negotiation_group_name,
                {
                    "type": "message_deleted",
                    "command": "delete_message",
                    "message_id": str(message_obj.pk),
                }
            )
        except Message.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Message not found.'}))

    # --- END MODIFIED RECEIVE BLOCK ---

    # --- Broadcast handlers ---

    # Receive message from room group (NEW MESSAGE)
    def chat_message(self, event):
        print(f"BROADCAST: Sending new message {event['message_id']} to client.")
        self.send(text_data=json.dumps(event))

    # NEW: Receive edited message from room group
    def message_edited(self, event):
        print(f"BROADCAST: Sending edited message {event['message_id']} to client.")
        self.send(text_data=json.dumps(event))

    # NEW: Receive deleted message from room group
    def message_deleted(self, event):
        print(f"BROADCAST: Sending delete command for {event['message_id']} to client.")
        self.send(text_data=json.dumps(event))