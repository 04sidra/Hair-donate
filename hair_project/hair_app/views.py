from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import HairDonor, HairRequest, DonationMatch, ContactMessage, UserProfile
from .forms import (UserRegistrationForm, HairDonorForm, HairRequestForm, ContactForm,
                    UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm)

def home(request):
    """Home page with statistics"""
    total_donors = HairDonor.objects.filter(status='Available').count()
    total_requests = HairRequest.objects.filter(request_status='Pending').count()
    total_matches = DonationMatch.objects.filter(donation_completed=True).count()
    
    context = {
        'total_donors': total_donors,
        'total_requests': total_requests,
        'total_matches': total_matches,
    }
    return render(request, 'hair_app/home.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Hair Donation Portal.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'hair_app/registration/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'hair_app/registration/login.html')


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def donor_registration(request):
    """Hair donor registration form"""
    if request.method == 'POST':
        form = HairDonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            if request.user.is_authenticated:
                donor.user = request.user
            donor.save()
            messages.success(request, 'Thank you for registering as a hair donor! Your kindness will help someone in need.')
            return redirect('donor_list')
    else:
        form = HairDonorForm()
    return render(request, 'hair_app/donor/donor_registration.html', {'form': form})


def donor_list(request):
    """List of available hair donors"""
    donors = HairDonor.objects.filter(status='Available').order_by('-hair_length')
    
    # Filter functionality
    city = request.GET.get('city')
    hair_color = request.GET.get('hair_color')
    min_length = request.GET.get('min_length')
    
    if city:
        donors = donors.filter(city__icontains=city)
    if hair_color:
        donors = donors.filter(hair_color=hair_color)
    if min_length:
        donors = donors.filter(hair_length__gte=min_length)
    
    context = {
        'donors': donors,
        'hair_colors': HairDonor.HAIR_COLOR_CHOICES,
    }
    return render(request, 'hair_app/donor/donor_list.html', context)


def request_hair(request):
    """Hair request form for patients"""
    if request.method == 'POST':
        form = HairRequestForm(request.POST, request.FILES)
        if form.is_valid():
            hair_request = form.save(commit=False)
            if request.user.is_authenticated:
                hair_request.user = request.user
            hair_request.save()
            messages.success(request, 'Your hair request has been submitted successfully. We will contact you soon.')
            return redirect('request_list')
    else:
        form = HairRequestForm()
    return render(request, 'hair_app/request/request_hair.html', {'form': form})


def request_list(request):
    """List of hair requests"""
    requests = HairRequest.objects.exclude(request_status='Fulfilled').order_by('-urgency', '-created_at')
    
    # Filter functionality
    patient_type = request.GET.get('patient_type')
    urgency = request.GET.get('urgency')
    city = request.GET.get('city')
    
    if patient_type:
        requests = requests.filter(patient_type=patient_type)
    if urgency:
        requests = requests.filter(urgency=urgency)
    if city:
        requests = requests.filter(city__icontains=city)
    
    context = {
        'requests': requests,
        'patient_types': HairRequest.PATIENT_TYPE_CHOICES,
        'urgency_levels': HairRequest.URGENCY_CHOICES,
    }
    return render(request, 'hair_app/request/request_list.html', context)


def request_detail(request, pk):
    """Detail view of a hair request"""
    hair_request = get_object_or_404(HairRequest, pk=pk)
    
    # Find matching donors
    matching_donors = HairDonor.objects.filter(
        status='Available',
        hair_length__gte=hair_request.required_hair_length
    )
    
    if hair_request.preferred_hair_color:
        matching_donors = matching_donors.filter(hair_color__icontains=hair_request.preferred_hair_color)
    
    context = {
        'request': hair_request,
        'matching_donors': matching_donors[:5],
    }
    return render(request, 'hair_app/request/request_detail.html', context)


@login_required
def user_profile(request):
    """User profile page"""
    # Get user's donor registrations
    donor_records = HairDonor.objects.filter(user=request.user)
    
    # Get user's requests
    user_requests = HairRequest.objects.filter(user=request.user)
    
    # Get donation matches
    donation_matches = DonationMatch.objects.filter(donor__user=request.user)
    
    context = {
        'donor_records': donor_records,
        'user_requests': user_requests,
        'donation_matches': donation_matches,
    }
    return render(request, 'hair_app/pages/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'hair_app/pages/edit_profile.html', context)


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'hair_app/pages/change_password.html', {'form': form})


@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            # Delete user account
            user.delete()
            messages.success(request, 'Your account has been deleted successfully. We\'re sad to see you go!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Account not deleted.')
    
    return render(request, 'hair_app/pages/delete_account.html')


@login_required
def my_donations(request):
    """User's donation history"""
    my_donor_records = HairDonor.objects.filter(user=request.user)
    my_donation_matches = DonationMatch.objects.filter(donor__user=request.user)
    
    context = {
        'donor_records': my_donor_records,
        'donation_matches': my_donation_matches,
    }
    return render(request, 'hair_app/donor/my_donations.html', context)


@login_required
def my_requests(request):
    """User's hair requests"""
    my_requests = HairRequest.objects.filter(user=request.user)
    
    context = {
        'requests': my_requests,
    }
    return render(request, 'hair_app/request/my_requests.html', context)


def about(request):
    """About page"""
    return render(request, 'hair_app/pages/about.html')


def contact(request):
    """Contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'hair_app/pages/contact.html', {'form': form})


def search(request):
    """Search functionality"""
    query = request.GET.get('q', '')
    
    donors = HairDonor.objects.filter(
        Q(full_name__icontains=query) | 
        Q(city__icontains=query) |
        Q(hair_color__icontains=query)
    ).filter(status='Available')
    
    requests = HairRequest.objects.filter(
        Q(patient_name__icontains=query) |
        Q(city__icontains=query) |
        Q(patient_type__icontains=query)
    ).exclude(request_status='Fulfilled')
    
    context = {
        'query': query,
        'donors': donors,
        'requests': requests,
    }
    return render(request, 'hair_app/pages/search.html', context)