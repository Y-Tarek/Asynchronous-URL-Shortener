from celery import shared_task
from .models import ShortenedURL
from django.db.models import F
from django_ratelimit.decorators import is_ratelimited


@shared_task
def update_clicks(shortened_url):
    ShortenedURL.objects.filter(shortened_code=shortened_url).update(
        clicks=F("clicks") + 1
    )


def is_rate_limited(request,method,group):
    """Check if the request exceeds the rate limit."""
    return is_ratelimited(
        request,
        key="ip",
        rate="3/5m",
        method=method,
        increment=True,
        group=group,
    )
