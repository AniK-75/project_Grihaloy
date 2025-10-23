from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/negotiation/(?P<negotiation_pk>[0-9a-f-]+)/$", consumers.NegotiationConsumer.as_asgi()),
]