from django.contrib import admin
from .models import *

admin.site.site_header = 'Golden Grove Collections'
admin.site.site_title = 'Golden Grove Collections'
admin.site.index_title = 'Golden Grove Collections'

# admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Region)
admin.site.register(Order)
admin.site.register(Color)
admin.site.register(Size)