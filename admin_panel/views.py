from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from uzhavan_hub.models import Farmer, Produce, UzhavanHub
from consumer_app.models import Consumer, Order, CartItem
from .models import Dispute, Notification
from .forms import HubForm, DisputeResolutionForm

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    farmers = Farmer.objects.count()
    consumers = Consumer.objects.count()
    hubs = UzhavanHub.objects.count()
    pending_orders = Order.objects.filter(status='P').count()
    
    context = {
        'farmers': farmers,
        'consumers': consumers,
        'hubs': hubs,
        'pending_orders': pending_orders,
    }
    return render(request, 'admin_panel/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def farmer_list(request):
    farmers = Farmer.objects.all().order_by('-registration_date')
    return render(request, 'admin_panel/farmer_list.html', {'farmers': farmers})

@login_required
@user_passes_test(is_admin)
def verify_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, pk=farmer_id)
    farmer.verified = not farmer.verified
    farmer.save()
    
    action = "verified" if farmer.verified else "unverified"
    messages.success(request, f'Farmer {action} successfully!')
    return redirect('farmer_list')

@login_required
@user_passes_test(is_admin)
def consumer_list(request):
    consumers = Consumer.objects.all().order_by('-user__date_joined')
    return render(request, 'admin_panel/consumer_list.html', {'consumers': consumers})

@login_required
@user_passes_test(is_admin)
def manage_hubs(request):
    hubs = UzhavanHub.objects.all().order_by('name')
    return render(request, 'admin_panel/manage_hubs.html', {'hubs': hubs})

@login_required
@user_passes_test(is_admin)
def add_hub(request):
    if request.method == 'POST':
        form = HubForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hub added successfully!')
            return redirect('manage_hubs')
    else:
        form = HubForm()
    
    return render(request, 'admin_panel/add_hub.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_hub(request, hub_id):
    hub = get_object_or_404(UzhavanHub, pk=hub_id)
    
    if request.method == 'POST':
        form = HubForm(request.POST, instance=hub)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hub updated successfully!')
            return redirect('manage_hubs')
    else:
        form = HubForm(instance=hub)
    
    return render(request, 'admin_panel/edit_hub.html', {'form': form, 'hub': hub})

@login_required
@user_passes_test(is_admin)
def dispute_list(request):
    disputes = Dispute.objects.filter(status='O').order_by('-created_at')
    return render(request, 'admin_panel/dispute_list.html', {'disputes': disputes})

@login_required
@user_passes_test(is_admin)
def resolve_dispute(request, dispute_id):
    dispute = get_object_or_404(Dispute, pk=dispute_id)
    
    if request.method == 'POST':
        form = DisputeResolutionForm(request.POST, instance=dispute)
        if form.is_valid():
            dispute = form.save(commit=False)
            dispute.status = 'R'
            dispute.resolved_at = timezone.now()
            dispute.save()
            
            # Create notification
            Notification.objects.create(
                recipient=dispute.raised_by.user,
                notification_type='D',
                message=f'Your dispute #{dispute.id} has been resolved',
                related_object_id=dispute.id
            )
            
            messages.success(request, 'Dispute resolved successfully!')
            return redirect('dispute_list')
    else:
        form = DisputeResolutionForm(instance=dispute)
    
    return render(request, 'admin_panel/resolve_dispute.html', {
        'form': form,
        'dispute': dispute
    })

@login_required
@user_passes_test(is_admin)
def sales_report(request):
    # Basic sales report - can be enhanced with date filters, charts, etc.
    orders = Order.objects.filter(status='D').order_by('-order_date')
    total_sales = sum(order.total_amount for order in orders)
    
    context = {
        'orders': orders,
        'total_sales': total_sales,
    }
    return render(request, 'admin_panel/sales_report.html', context)

@login_required
@user_passes_test(is_admin)
def inventory_report(request):
    produces = Produce.objects.filter(available=True).order_by('-quantity')
    return render(request, 'admin_panel/inventory_report.html', {'produces': produces})