from django.contrib.auth.models import AbstractUser
from django.db import models


class Bids(models.Model):
    current_bid = models.IntegerField(default=0)
    bid_number = models.IntegerField(default=0)
    highest_bidder = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        if self.current_bid > 0:
            return f"{self.bid_number} so far. Current bid is {self.current_bid}"
        else:
            return f"{self.bid_number} so far. There is no current bid."


class User(AbstractUser):
    pass


class Comments(models.Model):
    commentor = models.CharField(max_length=64, blank=True, null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return f"{self.commentor} \n {self.comment}"
        
        
class AuctionListings(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(max_length=64)
    description = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=10000,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    bids = models.ForeignKey(Bids, on_delete=models.CASCADE,blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True)
    creator = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    comment = models.ManyToManyField(Comments, blank=True, null=True)
