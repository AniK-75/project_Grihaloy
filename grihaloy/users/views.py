from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, VerificationDocumentForm, RatingForm
from .models import VerificationDocument, Rating, CustomUser

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home:index')  # change to your homepage URL name
        else:
            messages.error(request, "Please correct errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home:index')
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('home:index')

# VerificationDocument views
@login_required
def verification_list(request):
    if request.user.role == 'ADMIN' or request.user.is_superuser:
        docs = VerificationDocument.objects.all().order_by('-created_at')
    else:
        docs = request.user.verification_docs.all().order_by('-created_at')
    return render(request, 'users/verification_list.html', {'docs': docs})

@login_required
def verification_create(request):
    if request.method == 'POST':
        form = VerificationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            messages.success(request, "Document uploaded.")
            return redirect('users:verification_list')
    else:
        form = VerificationDocumentForm()
    return render(request, 'users/verification_form.html', {'form': form})

@login_required
def verification_delete(request, pk):
    doc = get_object_or_404(VerificationDocument, pk=pk)
    if doc.user != request.user and not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, "Not allowed.")
        return redirect('users:verification_list')
    doc.delete()
    messages.success(request, "Document deleted.")
    return redirect('users:verification_list')

# Admin approves/rejects (simple example)
@login_required
def verification_change_status(request, pk, status):
    if not (request.user.role == 'ADMIN' or request.user.is_superuser):
        messages.error(request, "Permission denied.")
        return redirect('users:verification_list')
    doc = get_object_or_404(VerificationDocument, pk=pk)
    if status in [VerificationDocument.APPROVED, VerificationDocument.REJECTED, VerificationDocument.PENDING]:
        doc.status = status
        doc.save()
        messages.success(request, f"Status set to {status}.")
    return redirect('users:verification_list')

# Ratings
@login_required
def rating_list(request, user_id=None):
    if user_id:
        ratings = Rating.objects.filter(rated__id=user_id).order_by('-created_at')
    else:
        ratings = request.user.given_ratings.all().order_by('-created_at')
    return render(request, 'users/rating_list.html', {'ratings': ratings})

@login_required
def rating_create(request, rated_id):
    rated_user = get_object_or_404(CustomUser, pk=rated_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = request.user
            rating.rated = rated_user
            rating.save()
            messages.success(request, "Rating submitted.")
            return redirect('users:rating_list', user_id=rated_id)
    else:
        form = RatingForm()
    return render(request, 'users/rating_form.html', {'form': form, 'rated': rated_user})
