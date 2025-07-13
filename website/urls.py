from django.urls import path

from .views import *
app_name = 'website'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('collection/', CollectionView.as_view(), name='collection'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('my-cart/', MyCartView.as_view(), name='my-cart'),
    path('my-cart/remove_item/<int:item_id>/', RemoveCartItemView.as_view(), name='remove_item'),
    path('my-cart/update_quantity/<int:item_id>/', UpdateQuantityView.as_view(), name='update_cart_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/place-order/', PlaceOrderView.as_view(), name='place_order'),
    path('checkout/complete_order/', CompleteOrderView.as_view(), name='complete_order'),
    path('paypal-return/', paypal_return, name='paypal_return'),
    path('paypal-cancel/', paypal_cancel, name='paypal_cancel'),
    path('user-dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('user-dashboard/profile_update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('product-details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
]