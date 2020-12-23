from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<str:listing_id>", views.get_listing, name="get_listing"),
    path("categories", views.get_categories, name="categories"),
    path(
        "category/<str:category_id>",
        views.get_categories_listings,
        name="category_listings",
    ),
]
