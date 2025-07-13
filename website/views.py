from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from paypalrestsdk import Payment
import paypalrestsdk
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import CreateView
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Adombisege.utils.decorators import MustLogin
from dashboard.forms import OrderAddressForm
from dashboard.models import Contact, Order, OrderAddressInfo, OrderItems, Product, Category, Cart, Region
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator

# paypalrestsdk.configure({
#     "mode": settings.PAYPAL_MODE,  # sandbox or live
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_CLIENT_SECRET,
# })

class HomePageView(View):
    template_name = 'pages/home.html'
    
    def get(self, request):
        categories = Category.objects.all()[:3]
        products = Product.objects.filter(category__in=categories, status= 'Published').order_by('-created_at')[:20]
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0 
        context = {
            'categories' : categories,
            'products' : products,
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
        }
        return render(request, self.template_name, context)
    
class SearchView(View):
    template_name = 'pages/search_result.html'
    
    def get(self, request):
        user = request.user
        keyword = request.GET.get('keyword')
        category_id = request.GET.get('category')
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        if keyword:
            products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword) | Q(category__id=category_id), status= 'Published') if category_id else Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword), status= 'Published')
            paginator = Paginator(products, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            categories = Category.objects.all()
            my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
            context = {
                'products' : page_obj,
                'my_cart' : my_cart,
                'categories' : categories,
                'cart_sub_total' : cart_sub_total,
            }
            return render(request, self.template_name,context)
    
class CollectionView(View):
    template_name = 'pages/collection.html'
    
    def get(self, request):
        user = request.user
        sort_by = request.GET.get('sort_by')
        category_name = request.GET.get('category_name')
        category_id = Category.objects.get(name=category_name).id if category_name else None
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        if sort_by or category_id:
            products = Product.objects.filter(status= 'Published')
            if category_id:
                products = products.filter(category_id=category_id)
            if sort_by == 'price_low_to_high':
                products = products.order_by('regular_price')
            elif sort_by == 'price_high_to_low':
                products = products.order_by('-regular_price')
            elif sort_by == 'newest_first':
                products = products.order_by('-created_at')
            elif sort_by == 'oldest_first':
                products = products.order_by('created_at')
            paginator = Paginator(products, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            user = request.user
            my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
            categories = Category.objects.all()
            context = {
                'products' : page_obj,
                'my_cart' : my_cart,
                'categories' : categories,
                'cart_sub_total' : cart_sub_total,
            }
            return render(request, self.template_name,context)
        products = Product.objects.filter(status= 'Published').order_by('-created_at')
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        categories = Category.objects.all()
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        context = {
            'products' : page_obj,
            'categories' : categories,
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
        }
        return render(request, self.template_name,context)
    

class ContactView(View):
    template_name = 'pages/contact.html'
    
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('website:contact') 
        else:
            messages.error(request, 'An error occurred while sending your message. Please ensure all fields are filled out correctly.')
        
        # In case of errors, re-render the page with the existing form data
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart': my_cart,
            'cart_sub_total': cart_sub_total,
            'categories': categories,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        return render(request, self.template_name, context)
class AboutUsView(View):
    template_name = 'pages/about-us.html'
    
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class FaqView(View):
    template_name = 'pages/faq.html'
    
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class PrivacyPolicyView(View):
    template_name = 'pages/privacy_policy.html'
    
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class ProductDetailView(View):
    template_name = 'pages/product_details.html'
    
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'product' : product,
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class AddToCartView(View):
    @method_decorator(MustLogin)
    def post(self, request):
        user = request.user
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)
        # Check if the product is already in the user's cart
        cart_item = Cart.objects.filter(user=user, product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, 'Product quantity updated successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            # If the product is not in the user's cart, create a new order item
            cart_item = Cart.objects.create(
                user=user,
                product=product,
                size = size,
                color = color,
                quantity = quantity
            )
            messages.success(request, 'Product added to cart successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class MyCartView(View):
    template_name = 'pages/cart.html'
    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
            
        }
        return render(request, self.template_name,context)
    
class RemoveCartItemView(View):
    @method_decorator(MustLogin)
    def get(self, request, item_id):
        # Retrieve the order item from the database
        order_item = get_object_or_404(Cart, id=item_id)
        
        # Delete the order item
        order_item.delete()
        
        # Return a JSON response indicating success and reload the page
        messages.success(request, 'Order item deleted from cart successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@method_decorator(csrf_exempt, name='dispatch')
class UpdateQuantityView(View):
    @method_decorator(MustLogin)
    def post(self, request, item_id):
        new_quantity = request.POST.get('new_quantity')

        try:
            # Update the quantity for the order item
            order_item = Cart.objects.get(id=item_id)
            order_item.quantity = new_quantity
            order_item.save()
            messages.success(request, 'Quantity updated successfully')
            return JsonResponse({'success': True})
        except (Cart.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'error': 'Failed to update quantity'}, status=400)
    
class CheckoutView(View):
    template_name = 'pages/checkout.html'
    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        regions = Region.objects.filter(is_active=True)
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'regions' : regions,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class PlaceOrderView(CreateView):
    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        form = OrderAddressForm(request.POST)
        if form.is_valid():
            # Retrieve the user's cart
            cart = Cart.objects.filter(user=request.user)
            payment_method = request.POST.get('payment_method', 'Cash')
            # Add order items to the order

            # Create Order instance
            order = Order.objects.create(
                user=request.user,
                total_price=request.POST.get('total'),
                payment_method=payment_method,
                special_instructions=request.POST.get('special_instructions', None),
            )

            for item in cart:
                order_items = OrderItems.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                )
                order.order_items.add(order_items)

            # Retrieve form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address_1 = form.cleaned_data['address_1']
            address_2 = form.cleaned_data['address_2']
            town_city = form.cleaned_data['town_city']
            region_id = form.cleaned_data['region']
            gps = form.cleaned_data['gps']

            # Create OrderAddressInfo instance
            order_address = OrderAddressInfo.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                address_1=address_1,
                address_2=address_2,
                town_city=town_city,
                region=region_id,
                gps=gps,
                order=order,
            )

            if payment_method == 'Online':
                messages.success(request, 'Your order has been placed successfully! Please proceed to make payment.')
                return redirect('website:complete_order')
                # Create PayPal payment
                # payment = Payment({
                #     "intent": "sale",
                #     "payer": {
                #         "payment_method": "paypal"
                #     },
                #     "redirect_urls": {
                #         "return_url": request.build_absolute_uri(reverse('website:paypal_return')),
                #         "cancel_url": request.build_absolute_uri(reverse('website:paypal_cancel')),
                #     },
                #     "transactions": [{
                #         "item_list": {
                #             "items": [{
                #                 "name": "Order #{}".format(order.id),
                #                 "sku": "order_{}".format(order.id),
                #                 "price": str(order.total_price),
                #                 "currency": "USD",
                #                 "quantity": 1
                #             }]
                #         },
                #         "amount": {
                #             "total": str(order.total_price),
                #             "currency": "USD"
                #         },
                #         "description": "Order #{}".format(order.id)
                #     }]
                # })

                # if payment.create():
                #     for link in payment.links:
                #         if link.rel == "approval_url":
                #             # Redirect the user to PayPal for payment approval
                #             return redirect(link.href)
                # else:
                #     messages.error(request, 'An error occurred while processing your PayPal payment. Please try again.')
                #     return redirect('website:checkout')

            # Clear the user's cart after placing the order
            cart.delete()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('website:complete_order')

        messages.error(request, 'An error occurred while processing your order. Please try again.')
        return redirect('website:checkout')

@csrf_exempt
def paypal_return(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment was successful
        messages.success(request, 'Your payment was successful!')
        return redirect('website:complete_order')
    else:
        messages.error(request, 'An error occurred while processing your PayPal payment. Please try again.')
        return redirect('website:checkout')

def paypal_cancel(request):
    messages.error(request, 'Your PayPal payment was canceled.')
    return redirect('website:checkout')
    
class CompleteOrderView(View):
    template_name = 'pages/complete-order.html'
    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories
        }
        return render(request, self.template_name,context)
    
class UserDashboardView(View):
    template_name = 'pages/user-dashboard.html'
    @method_decorator(MustLogin)
    def get(self, request):
        user = request.user
        my_cart = Cart.objects.filter(user=user) if user.is_authenticated else 0
        cart_sub_total = Cart.get_sub_total(user) if user.is_authenticated else 0
        categories = Category.objects.all()
        order_history = Order.objects.filter(user=user).order_by('-created_at')
        context = {
            'my_cart' : my_cart,
            'cart_sub_total' : cart_sub_total,
            'categories' : categories,
            'order_history' : order_history
        }
        return render(request, self.template_name,context)
    
class ProfileUpdateView(View):
    @method_decorator(MustLogin)
    def post(self, request):
        user = request.user
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        phone_number = request.POST.get('phone_number')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        if current_password and new_password and confirm_password:
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
                return render(request, 'profile_update.html', {'user': user})

            if new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
                return render(request, 'profile_update.html', {'user': user})

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))