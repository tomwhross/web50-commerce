""" To pass context to all views """
from django.contrib.auth.decorators import login_required

from .models import Watchlist


def add_watchlist_count_to_context(request):
    """ Adds the user's watchlist count on every view for layout/navbar """

    if request.user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(
            user=request.user, deleted=False
        ).count()

        return {
            "watchlist_count": watchlist_count,
        }

    return {"watchlist_count": None}
