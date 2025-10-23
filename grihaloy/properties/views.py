from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# FIX: Import Negotiation and Message models
from .forms import PropertyForm, PropertySearchForm, EditRequestForm, DeleteRequestForm
from .models import Property, PropertyPhoto, PropertyEditRequest, PropertyDeleteRequest, Negotiation, Message


def is_admin(user):
    return getattr(user, 'role', '') == 'ADMIN' or user.is_superuser or user.is_staff


def is_landlord(user):
    return getattr(user, 'role', '') == 'LANDLORD'


def is_renter(user):  # NEW
    return getattr(user, 'role', '') == 'RENTER'


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12

    def get_queryset(self):
        qs = Property.objects.select_related('owner').filter(is_active=True).prefetch_related('photos')
        form = PropertySearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            area = form.cleaned_data.get('area')
            city = form.cleaned_data.get('city')
            ptype = form.cleaned_data.get('property_type')
            min_p = form.cleaned_data.get('min_price')
            max_p = form.cleaned_data.get('max_price')
            ordering = form.cleaned_data.get('ordering') or '-created_at'

            if q:
                qs = qs.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(address__icontains=q) |
                    Q(area__icontains=q) |
                    Q(city__icontains=q)
                )
            if area:
                qs = qs.filter(area__icontains=area)
            if city:
                qs = qs.filter(city__iexact=city)
            if ptype:
                qs = qs.filter(property_type__iexact=ptype)
            if min_p is not None:
                qs = qs.filter(price__gte=min_p)
            if max_p is not None:
                qs = qs.filter(price__lte=max_p)

            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = PropertySearchForm(self.request.GET or None)
        # Preserve filters across pagination
        q = self.request.GET.copy()
        if 'page' in q:
            q.pop('page')
        ctx['querystring'] = q.urlencode()
        return ctx


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_queryset(self):
        qs = super().get_queryset().select_related('owner').prefetch_related('photos')
        user = self.request.user
        if is_admin(user):
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_active=True) | Q(owner=user))
        return qs.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        prop = self.object
        ctx['can_edit'] = user.is_authenticated and (
                    (prop.owner_id == user.id and prop.owner_can_edit) or is_admin(user))
        ctx['can_request_edit'] = user.is_authenticated and (prop.owner_id == user.id) and not prop.owner_can_edit
        ctx['can_toggle'] = user.is_authenticated and ((prop.owner_id == user.id) or is_admin(user))
        ctx['can_delete'] = user.is_authenticated and is_admin(user)

        # NEW: Negotiation related context
        ctx['can_start_negotiation'] = False
        ctx['existing_negotiation_id'] = None
        if user.is_authenticated and is_renter(user) and prop.negotiable and prop.is_active and prop.owner != user:
            negotiation = Negotiation.objects.filter(property=prop, renter=user).first()
            if negotiation:
                ctx['existing_negotiation_id'] = negotiation.pk
            else:
                ctx['can_start_negotiation'] = True
        elif user.is_authenticated and prop.owner == user and prop.negotiable:
            # Landlord can see if there are negotiations for their property
            ctx['has_active_negotiations_as_landlord'] = Negotiation.objects.filter(property=prop,
                                                                                    is_active=True).exists()
            ctx['landlord_negotiations'] = Negotiation.objects.filter(property=prop, is_active=True).order_by(
                '-updated_at')

        return ctx


class LandlordOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if is_admin(user):
            return True
        return is_landlord(user) and getattr(user, 'is_approved', False)

    def handle_no_permission(self):
        user = self.request.user
        if user.is_authenticated and is_landlord(user) and not is_admin(user):
            messages.error(self.request, "Your account is not approved yet. You cannot add a property.")
            return redirect('users:profile_detail', username=user.username)
        return super().handle_no_permission()


class OwnerOrAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        prop = self.get_object()
        return self.request.user.is_authenticated and (
                (prop.owner_id == self.request.user.id and prop.owner_can_edit) or is_admin(self.request.user)
        )


class PropertyCreateView(LandlordOrAdminRequiredMixin, LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:my')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = True
        ctx['photo_error'] = kwargs.get('photo_error')
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        images = request.FILES.getlist('images')
        if not images:
            return self.render_to_response(
                self.get_context_data(form=form, photo_error='Please upload at least one photo.'))
        if form.is_valid():
            return self.forms_valid(form, images)
        return self.render_to_response(self.get_context_data(form=form))

    def forms_valid(self, form, images):
        with transaction.atomic():
            obj = form.save(commit=False)
            obj.owner = self.request.user
            obj.owner_can_edit = False
            obj.save()
            for img in images:
                PropertyPhoto.objects.create(property=obj, image=img)
        messages.success(self.request, 'Property posted with photos! Editing is locked. Request edit if needed.')
        return redirect(self.success_url)


class PropertyUpdateView(OwnerOrAdminRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'
    success_url = reverse_lazy('properties:my')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['is_create'] = False
        ctx['photos'] = self.object.photos.all()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        images = request.FILES.getlist('images')
        if form.is_valid():
            return self.forms_valid(form, images)
        return self.render_to_response(self.get_context_data(form=form))

    def forms_valid(self, form, images):
        with transaction.atomic():
            obj = form.save()
            for img in images:
                PropertyPhoto.objects.create(property=obj, image=img)
            if not is_admin(self.request.user) and obj.owner_id == self.request.user.id:
                obj.owner_can_edit = False
                obj.last_owner_edit_at = timezone.now()
                obj.save(update_fields=['owner_can_edit', 'last_owner_edit_at'])
        messages.success(self.request, 'Changes saved. Editing locked again.')
        return redirect(self.success_url)


class PropertyDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('properties:list')

    def test_func(self):
        return is_admin(self.request.user)


class MyPropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_my_list.html'
    context_object_name = 'properties'
    paginate_by = 12

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).order_by('-created_at').prefetch_related('photos')


@login_required
def property_deactivate(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner_id != request.user.id and not is_admin(request.user):
        return HttpResponseForbidden('Only the owner or admin can deactivate this listing.')
    if request.method == 'POST':
        prop.is_active = False
        prop.save(update_fields=['is_active'])
        messages.info(request, 'Listing deactivated.')
    return redirect('properties:detail', pk=prop.pk)


@login_required
def property_activate(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner_id != request.user.id and not is_admin(request.user):
        return HttpResponseForbidden('Only the owner or admin can activate this listing.')
    if request.method == 'POST':
        prop.is_active = True
        prop.save(update_fields=['is_active'])
        messages.success(request, 'Listing activated.')
    return redirect('properties:detail', pk=prop.pk)


@login_required
def property_photo_delete(request, pk, photo_id):
    prop = get_object_or_404(Property, pk=pk)
    photo = get_object_or_404(PropertyPhoto, pk=photo_id, property=prop)
    if not (is_admin(request.user) or (prop.owner_id == request.user.id and prop.owner_can_edit)):
        return HttpResponseForbidden('Not allowed.')
    if request.method == 'POST':
        if prop.photos.count() <= 1:
            messages.error(request, 'At least one photo is required. Upload another before deleting this one.')
            return redirect('properties:edit', pk=prop.pk)
        photo.image.delete(save=False)
        photo.delete()
        messages.success(request, 'Photo deleted.')
    return redirect('properties:edit', pk=prop.pk)


@login_required
def request_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner_id != request.user.id:
        return HttpResponseForbidden('Only the owner can request edits.')
    if prop.owner_can_edit:
        messages.info(request, 'Editing is already unlocked.')
        return redirect('properties:edit', pk=prop.pk)

    existing_pending = PropertyEditRequest.objects.filter(property=prop, requester=request.user,
                                                          status='pending').first()
    if request.method == 'POST':
        form = EditRequestForm(request.POST)
        if form.is_valid():
            if existing_pending:
                messages.warning(request, 'You already have a pending edit request.')
                return redirect('properties:detail', pk=prop.pk)
            req = form.save(commit=False)
            req.property = prop
            req.requester = request.user
            req.save()
            messages.success(request, 'Edit request submitted. Admin will review.')
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = EditRequestForm()

    return render(request, 'properties/edit_request_form.html', {'form': form, 'property': prop})


@login_required
def request_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner_id != request.user.id:
        return HttpResponseForbidden('Only the owner can request deletion.')
    existing_pending = PropertyDeleteRequest.objects.filter(property=prop, requester=request.user,
                                                            status='pending').first()
    if request.method == 'POST':
        form = DeleteRequestForm(request.POST)
        if form.is_valid():
            if existing_pending:
                messages.warning(request, 'You already have a pending delete request for this property.')
                return redirect('properties:detail', pk=prop.pk)
            req = form.save(commit=False)
            req.property = prop
            req.requester = request.user
            req.save()
            messages.success(request, 'Delete request submitted. Admin will review.')
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = DeleteRequestForm()
    return render(request, 'properties/delete_request_form.html', {'form': form, 'property': prop})


@user_passes_test(is_admin)
def edit_request_list(request):
    edit_reqs = PropertyEditRequest.objects.select_related('property', 'requester').order_by('-created_at')
    del_reqs = PropertyDeleteRequest.objects.select_related('property', 'requester').order_by('-created_at')
    return render(request, 'properties/admin_requests_list.html', {
        'edit_requests': edit_reqs,
        'delete_requests': del_reqs,
    })


@user_passes_test(is_admin)
def approve_edit_request(request, request_id):
    req = get_object_or_404(PropertyEditRequest, pk=request_id)
    if req.status != 'pending':
        messages.info(request, 'This request was already processed.')
        return redirect('properties:requests')
    if request.method == 'POST':
        note = request.POST.get('admin_note', '').strip()
        req.status = 'approved'
        req.admin_note = note
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.save()
        prop = req.property
        prop.owner_can_edit = True
        prop.save(update_fields=['owner_can_edit'])
        messages.success(request, 'Approved. Owner can edit now.')
    return redirect('properties:requests')


@user_passes_test(is_admin)
def reject_edit_request(request, request_id):
    req = get_object_or_404(PropertyEditRequest, pk=request_id)
    if req.status != 'pending':
        messages.info(request, 'This request was already processed.')
        return redirect('properties:requests')
    if request.method == 'POST':
        note = request.POST.get('admin_note', '').strip()
        req.status = 'rejected'
        req.admin_note = note
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.save()
        messages.warning(request, 'Edit request rejected.')
    return redirect('properties:requests')


@user_passes_test(is_admin)
def approve_delete_request(request, request_id):
    req = get_object_or_404(PropertyDeleteRequest, pk=request_id)
    if req.status != 'pending':
        messages.info(request, 'This request was already processed.')
        return redirect('properties:requests')
    if request.method == 'POST':
        note = request.POST.get('admin_note', '').strip()
        # --- START FIX ---
        # The line below was: req.status =.approved'
        req.status = 'approved'
        # --- END FIX ---
        req.admin_note = note
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.save()
        if req.property:
            req.property.delete()
        messages.success(request, 'Delete request approved and listing deleted.')
    return redirect('properties:requests')


@user_passes_test(is_admin)
def reject_delete_request(request, request_id):
    req = get_object_or_404(PropertyDeleteRequest, pk=request_id)
    if req.status != 'pending':
        messages.info(request, 'This request was already processed.')
        return redirect('properties:requests')
    if request.method == 'POST':
        note = request.POST.get('admin_note', '').strip()
        req.status = 'rejected'
        req.admin_note = note
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.save()
        messages.warning(request, 'Delete request rejected.')
    return redirect('properties:requests')


# --- START MODIFIED 'notifications' VIEW ---
@login_required
def notifications(request):
    """
    Show all notifications:
    1. Approved/rejected edit/delete requests.
    2. Unread negotiation messages.
    """
    edit_requests = PropertyEditRequest.objects.filter(
        requester=request.user,
        status__in=['approved', 'rejected']
    ).select_related('property').order_by('-reviewed_at', '-created_at')

    delete_requests = PropertyDeleteRequest.objects.filter(
        requester=request.user,
        status__in=['approved', 'rejected']
    ).select_related('property').order_by('-reviewed_at', '-created_at')

    account_status = 'Approved' if getattr(request.user, 'is_approved', False) or is_admin(request.user) else 'Pending'

    # FIX: Query for unseen negotiations to display them on the page
    unseen_negotiations = []
    if is_renter(request.user):
        unseen_negotiations = Negotiation.objects.filter(
            renter=request.user,
            is_active=True,
            seen_by_renter=False
        ).select_related('property', 'landlord').order_by('-updated_at')
    elif is_landlord(request.user):
        unseen_negotiations = Negotiation.objects.filter(
            landlord=request.user,
            is_active=True,
            seen_by_landlord=False
        ).select_related('property', 'renter').order_by('-updated_at')
    # END FIX

    # Mark edit/delete notifications as seen (this is correct)
    # DO NOT mark negotiations as seen here. That happens in the chat view.
    PropertyEditRequest.objects.filter(requester=request.user, status__in=['approved', 'rejected'],
                                       seen_by_requester=False).update(seen_by_requester=True)
    PropertyDeleteRequest.objects.filter(requester=request.user, status__in=['approved', 'rejected'],
                                         seen_by_requester=False).update(seen_by_requester=True)

    return render(request, 'properties/notifications.html', {
        'edit_requests': edit_requests,
        'delete_requests': delete_requests,
        'account_status': account_status,
        'unseen_negotiations': unseen_negotiations,  # FIX: Pass new variable to template
    })


# --- END MODIFIED 'notifications' VIEW ---

# NEW: Negotiation Views
@login_required
@user_passes_test(is_renter)
def start_negotiation(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    if not prop.negotiable:
        messages.error(request, 'This property is not open for negotiation.')
        return redirect('properties:detail', pk=prop.pk)

    if prop.owner == request.user:
        messages.error(request, "You cannot negotiate on your own property.")
        return redirect('properties:detail', pk=prop.pk)

    negotiation, created = Negotiation.objects.get_or_create(
        property=prop,
        renter=request.user,
        defaults={
            'landlord': prop.owner,
            'is_active': True,
            'seen_by_landlord': False,  # New negotiation is unseen by landlord
            'seen_by_renter': True,  # Renter just created it, so they've seen it
        }
    )

    if created:
        messages.success(request, 'Negotiation started! You can now chat with the landlord.')
    else:
        messages.info(request, 'You already have an active negotiation for this property.')

    return redirect('properties:negotiation_chat', pk=negotiation.pk)


@login_required
def negotiation_chat(request, pk):
    negotiation = get_object_or_404(Negotiation.objects.select_related('property__owner', 'renter'), pk=pk)

    if not (request.user == negotiation.renter or request.user == negotiation.landlord):
        return HttpResponseForbidden('You are not a participant in this negotiation.')

    messages_in_chat = negotiation.messages.select_related('sender').all()

    # Mark as seen when entering the chat
    if request.user == negotiation.landlord:
        if not negotiation.seen_by_landlord:
            negotiation.seen_by_landlord = True
            negotiation.save(update_fields=['seen_by_landlord'])
    elif request.user == negotiation.renter:
        if not negotiation.seen_by_renter:
            negotiation.seen_by_renter = True
            negotiation.save(update_fields=['seen_by_renter'])

    return render(request, 'properties/negotiation_chat.html', {
        'negotiation': negotiation,
        'messages': messages_in_chat,
        'current_user': request.user,
    })


@login_required
def my_negotiations(request):
    if is_landlord(request.user):
        negotiations = Negotiation.objects.filter(landlord=request.user, is_active=True).select_related('property',
                                                                                                        'renter').order_by(
            '-updated_at')
        unseen_count = Negotiation.objects.filter(landlord=request.user, is_active=True, seen_by_landlord=False).count()
    elif is_renter(request.user):
        negotiations = Negotiation.objects.filter(renter=request.user, is_active=True).select_related('property',
                                                                                                      'landlord').order_by(
            '-updated_at')
        unseen_count = Negotiation.objects.filter(renter=request.user, is_active=True, seen_by_renter=False).count()
    else:
        negotiations = []
        unseen_count = 0
        messages.info(request, "Only renters and landlords can have negotiations.")

    return render(request, 'properties/my_negotiations.html', {
        'negotiations': negotiations,
        'unseen_negotiations_count': unseen_count,
    })