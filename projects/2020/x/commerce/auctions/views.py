from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

categories = ["Clothing", "Electronics", "Food", "Home appliances", "Toys", "Games"]


def index(request):
    return render(request, "auctions/index.html",{
        "listings": AuctionListings.objects.all(),
        "category": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        current = request.user.username
        name = request.POST["name"]
        description = request.POST["description"]
        url = request.POST["url"]
        price = request.POST["price"]
        category = request.POST["cat"]
        bids = Bids.objects.create(current_bid=0, bid_number=0)
        listing = AuctionListings.objects.create(name=name,creator=current, category=category, description=description, url=url, price=price, bids=bids)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
            "message": "You should sign in to create a new listing",
            "category": categories,
        })

def listing(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "category": categories,
    "watch_btn": "Remove from watchlist...."
    })
               
def place_bid(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        bid_placed = request.POST["placed_bid"]
        if listing.bids == None:
            bids = Bids.objects.create(current_bid=0, bid_number=0)
            listing.bids = bids
        if int(bid_placed) >= int(listing.price) and int(bid_placed) > int(listing.bids.current_bid):
            listing.price = bid_placed
            listing.bids.current_bid = bid_placed
            listing.bids.bid_number += 1
            listing.bids.highest_bidder = request.user.username
            listing.save()
            listing.bids.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": categories,
                })
        else:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your need to place a higher bid.",
            "category": categories,
            })
    else:
        return render(request, "auctions/login.html")

def add_watchlist(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        current = request.user
        if current in listing.watchlist.all():
            listing.watchlist.remove(current)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": categories,
                })
        elif current not in listing.watchlist.all():
            listing.watchlist.add(current)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "category": categories,
                })
    else:
        return render(request, "auctions/login.html")

def remove_list(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": categories,
    })

def watchlist(request):
    current = request.user
    return render(request, "auctions/watchlist.html", {
        "watchlist": current.auctionlistings_set.all(),
        "category": categories,
        })

def cat_page(request):
    return render(request, "auctions/cat_page.html",{
        "categories": categories
    })
    
def category(request, category):
    cats = AuctionListings.objects.filter(category=category).all()
    print(cats)
    return render(request, "auctions/category.html", {
        "category": cats,
        "cat_name": category
    })
    
def add_comment(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    commentor = request.user.username
    commentt = request.POST["comment_value"]
    if commentt == "":
        return render(request, "auctions/listing.html",{
        "listing": listing,
        "com": "You cant post a blank comment"
    })
    else:
        comment = Comments.objects.create(comment=commentt, commentor=commentor)
        listing.comment.add(comment)
        return render(request, "auctions/listing.html",{
            "listing": listing
            })
    