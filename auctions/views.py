""" Views """

import decimal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Category, Comment, Listing, User


class ListingForm(forms.ModelForm):
    """ Form for creating Listings """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = "create_listing"
        self.helper.help_text_inline = True
        self.helper.add_input(Submit("submit", "Create Listing"))

    class Meta:
        model = Listing
        fields = ["category", "title", "description", "starting_bid", "image_url"]


class BidForm(forms.ModelForm):
    """ Form for placing Bids on Listings """

    def __init__(self, *args, **kwargs):
        high_bid = kwargs.pop("high_bid", None)
        listing_id = kwargs.pop("listing_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-myModelForm'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = listing_id
        self.helper.help_text_inline = True
        self.fields["amount"].widget.attrs["min"] = high_bid + decimal.Decimal(0.01)
        self.helper.add_input(Submit("submit", "Place Bid"))

    class Meta:
        model = Bid
        fields = [
            "amount",
        ]


class CommentForm(forms.ModelForm):
    """ Form for adding comments to Listings """

    def __init__(self, *args, **kwargs):
        listing_id = kwargs.pop("listing_id", None)
        # user_id = kwargs.pop("user_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-myModelForm'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = listing_id
        self.helper.help_text_inline = True
        self.helper.add_input(Submit("add_comment", "Add Comment"))

    class Meta:
        model = Comment
        fields = [
            "body",
        ]


class CloseListingForm(forms.ModelForm):
    """ Form for closing bids by the lister """

    def __init__(self, *args, **kwargs):
        listing_id = kwargs.pop("listing_id", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_id = 'id-myModelForm'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = listing_id
        self.helper.help_text_inline = True
        # self.fields["amount"].widget.attrs["min"] = high_bid + decimal.Decimal(0.01)
        self.helper.add_input(Submit("submit", "Close Auction"))

    class Meta:
        model = Listing
        fields = []


def index(request):
    """ Home page - Displays all active listings """

    listings = Listing.objects.filter(closed=False).order_by("-created_at", "-pk")

    return render(request, "auctions/index.html", {"listings": listings})


def get_listing(request, listing_id):
    """ Listing detail page - Allows users to place Bids on Listing """

    listing = Listing.objects.get(pk=listing_id)

    # if bidding user is not logged in, redirect to the login page
    # otherwise create a bid entry for the user if they are not the listing user
    # if they are the listing user, close the listing
    if request.method == "POST":
        # import pdb

        # pdb.set_trace()
        user = request.user

        if not user.is_authenticated:

            return HttpResponseRedirect(reverse("login"))

        if user.username != listing.user.username:
            bid_amount = request.POST["amount"]
            bid = Bid(amount=bid_amount, user=user, listing=listing)
            bid.save()
        else:
            listing.closed = True
            listing.save()

        # always redirect on post to prevent form resubmission on refresh!
        return HttpResponseRedirect(reverse("get_listing", args=(listing_id,)))

    # get the highest bid if one exists, otherwise display the starting bid
    # high_bid = listing.bids.all().order_by("-amount").first()
    high_bid_amount = listing.highest_bid_amount

    # don't form the bid form to the listing user
    # checking the usernames seems ok as django forces them to be unique
    # show the high bid user to the listing user instead
    bid_form = None
    close_listing_form = None
    high_bid_user = None
    if listing.bid_count > 1:
        bid_message = f"There are {listing.bid_count} bids on this listing"
    else:
        bid_message = f"There is {listing.bid_count} bid on this listing"

    if request.user.username != listing.user.username:
        bid_form = BidForm(high_bid=high_bid_amount, listing_id=listing_id)
        if request.user.username == listing.highest_bid_username:
            bid_message = f"{bid_message} (You have the highest bid)"

    else:
        # if high_bid is not None:
        #     high_bid_user = high_bid.user.username
        high_bid_user = listing.highest_bid_username
        if not listing.closed:
            close_listing_form = CloseListingForm(listing_id=listing_id)

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "high_bid": high_bid_amount,
            "high_bid_user": high_bid_user,
            "bid_form": bid_form,
            "bid_message": bid_message,
            "close_listing_form": close_listing_form,
            # "comment_form": CommentForm(listing_id=listing_id),
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):

    if request.method == "POST":
        category = Category.objects.get(pk=request.POST["category"])
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]
        user = request.user

        listing = Listing(
            title=title,
            description=description,
            category=category,
            user=user,
            image_url=image_url,
            starting_bid=starting_bid,
        )
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {"form": ListingForm()})
