from django.contrib import admin

# Register your models here.
from .models import Bid, Category, Comment, Listing, User, Watchlist

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)
