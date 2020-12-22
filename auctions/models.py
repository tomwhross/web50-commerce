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

    @property
    def highest_bid_username(self):
        """
        Return the highest bid amount if one exists, otherwise
        the starting bid amount
        """

        return self.bids.all().order_by("-amount").first().user.username or None

    @property
    def highest_bid_amount(self):
        """
        Returns the username of the user with the highest bid if one exists
        """

        return self.bids.all().order_by("-amount").first().amount or None


class Bid(models.Model):
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Bid Amount"
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):

        return f"{self.user.first_name}: {self.listing.title} - {self.amount}"