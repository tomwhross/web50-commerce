from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):

        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listings"
    )
    image_url = models.CharField(
        max_length=255, verbose_name="Image URL", null=True, blank=True
    )
    starting_bid = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Starting Bid Amount",
        null=True,
        blank=True,
        default=0,
    )
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.title}"

    def get_bids(self):
        """ Return all bids for listing """

        return self.bids.all()

    @property
    def bid_count(self):
        """ Returns the number of bids for a listing """

        return self.get_bids().count()

    def get_highest_bid(self):
        """ Returns the highest bid for a listing """

        return self.get_bids().order_by("-amount").first()

    @property
    def highest_bid(self):
        """ Returns the highest bid for a listing """

        return self.get_bids().order_by("-amount").first()

    @property
    def highest_bid_username(self):
        """
        Return the highest bid amount if one exists, otherwise
        the starting bid amount
        """

        try:
            return self.highest_bid.user.username
        except AttributeError:
            return None

    @property
    def highest_bid_amount(self):
        """
        Returns the username of the user with the highest bid if one exists
        """

        try:
            return self.highest_bid.amount
        except AttributeError:
            return self.starting_bid


class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} on {self.listing.title} at {self.created_at}"


class Bid(models.Model):
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Bid Amount"
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):

        return f"{self.user.first_name}: {self.listing.title} - {self.amount}"


class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watched_listings"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watched_listings"
    )
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):

        return f"{self.user.username} - {self.user.watched_listings.count()} watched listings"
