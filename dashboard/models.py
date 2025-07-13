import random
import string
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return self.image.url
            # return '/static/website/assets/men_category.png'
        else:
            return '/static/website/assets/img/category_image.png'

    def __str__(self):
        return self.name
    
    def get_product_count(self):
        return self.product_set.count()
    
    class Meta:
        verbose_name_plural = 'Categories'
        
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    STOCK_STATUS_CHOICES = (
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    )
    STATUS_CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size)
    colors = models.ManyToManyField(Color)  # Many-to-Many relationship with Color
    tag = models.CharField(max_length=100, null=True, blank=True)
    stock_status = models.CharField(max_length=100, choices=STOCK_STATUS_CHOICES, default='In Stock')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_price(self):
        '''Returns the price of the product'''
        return self.discount_price if self.discount_price else self.regular_price
    
    
    def get_image(self):
        if self.image:
            return self.image.url
            # return '/static/website/assets/project3.png'
        else:
            return '/static/website/assets/img/product_image.png'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Products'
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    
    class Meta:
        verbose_name_plural = 'Contacts'


class Cart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,related_name='my_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=10,blank=True, null=True)
    size = models.CharField(max_length=10,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        '''Returns the total price of the order item'''
        # Check if the product has a discount
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.regular_price * self.quantity if self.product.regular_price else 0
    
    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    @staticmethod
    def get_sub_total(user):
        '''Returns the total price of all items in the cart for a specific user'''
        cart_items = Cart.objects.filter(user=user)
        # if user has coupon applied
        # if cart_items.filter(coupon_applied=True).exists():
        #     return sum([item.get_discount_total() for item in cart_items])
        return sum([item.get_total() for item in cart_items])
    
class OrderItems(models.Model):
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    def get_total(self):
        '''Returns the total price of the order item'''
        # Check if the product has a discount
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.regular_price * self.quantity if self.product.regular_price else 0
    
    @staticmethod
    def get_sub_total(user):
        '''Returns the total price of all items in the cart for a specific user'''
        cart_items = Cart.objects.filter(user=user)
        # if user has coupon applied
        # if cart_items.filter(coupon_applied=True).exists():
        #     return sum([item.get_discount_total() for item in cart_items])
        return sum([item.get_total() for item in cart_items])
    
    class Meta:
        verbose_name_plural = 'Order Items'
    
class Order(models.Model):
    def generate_order_id() -> str:
        '''Generates a unique order id'''
        sub = 'AC-'
        return sub + ''.join(random.choices(string.digits, k=8))
    
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('Not Paid', 'Not Paid'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    )
    order_id = models.CharField(max_length=20, default=generate_order_id, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    order_items = models.ManyToManyField(OrderItems, related_name='order_items')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Not Paid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order from {self.user} - {self.order_id} - {self.status}'
    
    def get_order_items(self):
        return self.order_items.all()
    
    def get_total_price(self):
        total = 0
        for item in self.order_items.all():
            total += item.product.price * item.quantity
        return total
    
    class Meta:
        verbose_name_plural = 'Orders'

class Region(models.Model):
    name = models.CharField(max_length=100)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    
    def __str__(self):
        return self.name
        
class OrderAddressInfo(models.Model):
    '''Order address model'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="address_infos")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50,null=True,blank=True)
    town_city = models.CharField(max_length=100, null=True,blank=True)
    region = models.ForeignKey(Region,on_delete=models.DO_NOTHING, default=1)
    country = models.CharField(max_length=100, default="Ghana")
    gps = models.CharField(max_length=100, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order} - {self.address}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Address'
        verbose_name_plural = 'Order Addresses'

class Transaction(models.Model):
    def generate_transaction_id() -> str:
        '''Generates a unique transaction id'''
        sub = 'TR-'
        return sub + ''.join(random.choices(string.digits, k=8))
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending')
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='transactions')
    transaction_id = models.CharField(max_length=20, default=generate_transaction_id, unique=True)
    transaction_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.order} - {self.transaction_id} - {self.transaction_status}'
    
    class Meta:
        verbose_name_plural = 'Transactions'
