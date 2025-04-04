from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Farmer, Produce, UzhavanHub
from .forms import (FarmerRegistrationForm, ProduceForm, 
                   HubSubmissionForm, FarmerProfileForm,
                   HubCreationForm, HubEditForm)

def home(request):
    return render(request, 'home.html')

# Farmer Views
@login_required
def farmer_dashboard(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
        produces = Produce.objects.filter(farmer=farmer).order_by('-listed_at')
        context = {
            'farmer': farmer,
            'produces': produces
        }
        return render(request, 'uzhavan_hub/farmer_dashboard.html', context)
    except Farmer.DoesNotExist:
        return redirect('farmer_register')

def farmer_register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        farmer_form = FarmerRegistrationForm(request.POST)
        
        if user_form.is_valid() and farmer_form.is_valid():
            user = user_form.save()
            farmer = farmer_form.save(commit=False)
            farmer.user = user
            farmer.save()
            messages.success(request, 'Registration successful! Please wait for verification.')
            return redirect('login')
    else:
        user_form = UserCreationForm()
        farmer_form = FarmerRegistrationForm()
    
    return render(request, 'uzhavan_hub/farmer_register.html', {
        'user_form': user_form,
        'farmer_form': farmer_form
    })

@login_required
def farmer_profile(request):
    farmer = get_object_or_404(Farmer, user=request.user)
    
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('farmer_profile')
    else:
        form = FarmerProfileForm(instance=farmer)
    
    return render(request, 'uzhavan_hub/farmer_profile.html', {'form': form})

@login_required
def add_produce(request):
    farmer = get_object_or_404(Farmer, user=request.user)
    
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES)
        if form.is_valid():
            produce = form.save(commit=False)
            produce.farmer = farmer
            produce.save()
            messages.success(request, 'Produce added successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProduceForm()
    
    return render(request, 'uzhavan_hub/add_produce.html', {'form': form})

@login_required
def edit_produce(request, pk):
    produce = get_object_or_404(Produce, pk=pk, farmer__user=request.user)
    
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES, instance=produce)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produce updated successfully!')
            return redirect('farmer_dashboard')
    else:
        form = ProduceForm(instance=produce)
    
    return render(request, 'uzhavan_hub/edit_produce.html', {'form': form})

@login_required
def delete_produce(request, pk):
    produce = get_object_or_404(Produce, pk=pk, farmer__user=request.user)
    if request.method == 'POST':
        produce.delete()
        messages.success(request, 'Produce deleted successfully!')
    return redirect('farmer_dashboard')

# Hub Views
@login_required
def hub_list(request):
    hubs = UzhavanHub.objects.all().order_by('name')
    context = {
        'hubs': hubs,
        'can_manage': request.user.is_staff
    }
    return render(request, 'uzhavan_hub/hub_list.html', context)

@login_required
def hub_detail(request, hub_id):
    hub = get_object_or_404(UzhavanHub, pk=hub_id)
    produces = Produce.objects.filter(hub=hub, available=True).order_by('-listed_at')
    context = {
        'hub': hub,
        'produces': produces,
        'can_edit': request.user.is_staff or request.user == hub.manager
    }
    return render(request, 'uzhavan_hub/hub_detail.html', context)

@login_required
def create_hub(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = HubCreationForm(request.POST)
        if form.is_valid():
            hub = form.save()
            messages.success(request, f'Hub "{hub.name}" created successfully!')
            return redirect('hub_detail', hub_id=hub.id)
    else:
        form = HubCreationForm(initial={'manager': request.user})
    
    return render(request, 'uzhavan_hub/hub_form.html', {
        'form': form,
        'title': 'Create New Hub'
    })

@login_required
def edit_hub(request, hub_id):
    hub = get_object_or_404(UzhavanHub, pk=hub_id)
    
    # Only staff or hub manager can edit
    if not (request.user.is_staff or request.user == hub.manager):
        raise PermissionDenied
    
    if request.method == 'POST':
        form = HubEditForm(request.POST, instance=hub)
        if form.is_valid():
            hub = form.save()
            messages.success(request, f'Hub "{hub.name}" updated successfully!')
            return redirect('hub_detail', hub_id=hub.id)
    else:
        form = HubEditForm(instance=hub)
    
    return render(request, 'uzhavan_hub/hub_form.html', {
        'form': form,
        'title': f'Edit {hub.name}'
    })

@login_required
def submit_to_hub(request, produce_id):
    produce = get_object_or_404(Produce, pk=produce_id, farmer__user=request.user)
    
    if request.method == 'POST':
        form = HubSubmissionForm(request.POST)
        if form.is_valid():
            hub = form.cleaned_data['hub']
            produce.hub = hub
            produce.save()
            messages.success(request, f'Produce submitted to {hub.name} successfully!')
            return redirect('farmer_dashboard')
    else:
        form = HubSubmissionForm()
    
    return render(request, 'uzhavan_hub/submit_to_hub.html', {
        'form': form,
        'produce': produce
    })

@login_required
def hub_dashboard(request, hub_id):
    hub = get_object_or_404(UzhavanHub, pk=hub_id)
    
    # Only staff or hub manager can access dashboard
    if not (request.user.is_staff or request.user == hub.manager):
        raise PermissionDenied
    
    produces = Produce.objects.filter(hub=hub, available=True).order_by('-listed_at')
    farmers = Farmer.objects.filter(produce__hub=hub).distinct()
    
    context = {
        'hub': hub,
        'produces': produces,
        'farmers': farmers,
        'can_manage': request.user.is_staff
    }
    return render(request, 'uzhavan_hub/hub_dashboard.html', context)