from django.utils import timezone
from urllib import request
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from . models import Cart, Customer, Order, Product,OrderItem
from . forms import CustomerProfileForm,CustomerRegistrationForm, LoginForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


# Create your views here.

import logging

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with the name of the page you want to redirect to.
        return super().dispatch(request, *args, **kwargs)

def home(request):
    logger.info("Home view was accessed.")
    return render(request, 'app/home.html')

def about(request):
    return render(request,"app/about.html")

def contact(request):
    return render(request,"app/contact.html")

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())
    
    
class ProductDetail(View):
    def get(self,request,pk):
          product = Product.objects.get(pk=pk)
          return render(request, "app/productdetail.html",locals())
    
class CustomerregistrationView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to 'home' if the user is already logged in
        if request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with the actual name of your home URL
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, "app/Customerregistration.html",locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
             form.save()
             messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())
    

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, "app/profile.html", {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            # Assuming 'mobile' is another field in the form
            mobile = form.cleaned_data.get('mobile', '')
            
            # Create or update the customer profile
            Customer.objects.update_or_create(user=user, defaults={'name': name, 'mobile': mobile})
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile page after updating

        # If form is not valid, render the profile page with form errors
        return render(request, "app/profile.html", {'form': form})


def details(request):
    if request.user.is_authenticated:
        try:
            add, created = Customer.objects.get_or_create(user=request.user)
            if created:
                messages.info(request, "A new profile was created for you.")
            return render(request, 'app/details.html', {'add': add})
        except Customer.DoesNotExist:
            messages.warning(request, "No customer record found for this user.")
            return redirect('profile')
    else:
        messages.warning(request, "You need to be logged in to view details.")
        return redirect('login')



class Updatedetails(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, "app/updatedetails.html",locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name' ]
            add.mobile = form.cleaned_data['mobile' ]
            add. save()
            messages. success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("details")

@login_required
def add_to_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        
        
        if not product_id:
            messages.warning(request, "Product ID is missing.")
            return redirect('')  

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.warning(request, "Product does not exist.")
            return redirect('')

       
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1 
            cart_item.save()

        messages.success(request, f"{product.title} added to cart.")
        return redirect('cart')  # Redirect to the cart page

   
    messages.warning(request, "Invalid request method.")
    return redirect('')

@login_required
def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    # Calculating the total amount of items in the cart
    amount = sum(item.product.selling_price * item.quantity for item in cart_items)
    gst = 0.1 * amount  # Assuming GST as 10% of the amount
    totalamount = amount + gst  # Including GST

    # Rendering template with calculated values
    return render(request, 'app/addtocart.html', {
        'cart': cart_items,
        'amount': amount,
        'totalamount': totalamount
    })


@login_required
def remove_item(request, prod_id):
   
    product = get_object_or_404(Product, id=prod_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart_item:
        cart_item.delete()  
        messages.success(request, f"{product.title} has been removed from your cart.")
    else:
        messages.warning(request, "This item is not in your cart.") 
    return redirect("/cart")


@login_required
def place_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    total_amount = sum(item.product.selling_price * item.quantity for item in cart_items)

    # Create a new order
    order = Order.objects.create(user=user, total_amount=total_amount, created_at=timezone.now())
    # Create OrderItems from Cart items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.selling_price,
        )
    cart_items.delete() 
 
     # Clear the user's cart after placing the order

    messages.success(request, f"Order placed successfully! Order ID: {order.order_id}")
    return redirect('order_confirmation', order_id=order.order_id)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = order.orderitem_set.all()

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'app/orderconfirmation.html', {'order_id': order_id})

@login_required
def my_orders(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).prefetch_related('orderitem_set')

    return render(request, 'app/orders.html', {'orders': orders})


def delete_order(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('my_orders')
    else:
        return redirect('login')














        




    















   
