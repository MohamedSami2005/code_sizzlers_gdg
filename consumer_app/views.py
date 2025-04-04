from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from uzhavan_hub.models import Produce
from .models import Consumer, Cart, CartItem, Order
from .forms import ConsumerRegistrationForm, CheckoutForm

def marketplace(request):
    produces = Produce.objects.filter(available=True, approved=True).order_by('-listed_at')
    return render(request, 'consumer_app/marketplace.html', {'produces': produces})

def product_detail(request, pk):
    produce = get_object_or_404(Produce, pk=pk, available=True, approved=True)
    return render(request, 'consumer_app/product_detail.html', {'produce': produce})

def consumer_register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        consumer_form = ConsumerRegistrationForm(request.POST)
        
        if user_form.is_valid() and consumer_form.is_valid():
            user = user_form.save()
            consumer = consumer_form.save(commit=False)
            consumer.user = user
            consumer.save()
            messages.success(request, 'Registration successful! You can now shop.')
            return redirect('login')
    else:
        user_form = UserCreationForm()
        consumer_form = ConsumerRegistrationForm()
    
    return render(request, 'consumer_app/consumer_register.html', {
        'user_form': user_form,
        'consumer_form': consumer_form
    })

@login_required
def view_cart(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    cart, created = Cart.objects.get_or_create(consumer=consumer, is_active=True)
    return render(request, 'consumer_app/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, produce_id):
    produce = get_object_or_404(Produce, pk=produce_id, available=True, approved=True)
    consumer = get_object_or_404(Consumer, user=request.user)
    cart, created = Cart.objects.get_or_create(consumer=consumer, is_active=True)
    
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than zero')
            return redirect('product_detail', pk=produce_id)
        
        if quantity > produce.quantity:
            messages.error(request, 'Not enough quantity available')
            return redirect('product_detail', pk=produce_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            produce=produce,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, 'Item added to cart successfully!')
        return redirect('view_cart')
    
    return render(request, 'consumer_app/add_to_cart.html', {'produce': produce})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__consumer__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('view_cart')

@login_required
def checkout(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    cart = get_object_or_404(Cart, consumer=consumer, is_active=True)
    
    if not cart.cartitem_set.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('marketplace')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                consumer=consumer,
                cart=cart,
                delivery_address=form.cleaned_data['delivery_address'],
                contact_number=form.cleaned_data['contact_number'],
                payment_method=form.cleaned_data['payment_method'],
                total_amount=cart.total_amount(),
                payment_status=False  # Assuming cash on delivery for now
            )
            
            # Mark cart as inactive
            cart.is_active = False
            cart.save()
            
            # Update produce quantities
            for item in cart.cartitem_set.all():
                item.produce.quantity -= item.quantity
                if item.produce.quantity <= 0:
                    item.produce.available = False
                item.produce.save()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_history')
    else:
        initial_data = {
            'delivery_address': consumer.address,
            'contact_number': consumer.phone,
        }
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'consumer_app/checkout.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_history(request):
    consumer = get_object_or_404(Consumer, user=request.user)
    orders = Order.objects.filter(consumer=consumer).order_by('-order_date')
    return render(request, 'consumer_app/order_history.html', {'orders': orders})