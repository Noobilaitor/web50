from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
