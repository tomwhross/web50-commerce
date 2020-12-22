from django.contrib import admin

# Register your models here.
from .models import Bid, Category, Listing, User

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
