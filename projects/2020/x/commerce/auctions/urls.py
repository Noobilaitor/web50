from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("placebid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("addwatchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("removelist/<int:listing_id>", views.remove_list, name="remove_list"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("category/<str:category>", views.category, name="category"),
    path("cat_page", views.cat_page, name="cat_page"),
    path("register", views.register, name="register")
]
