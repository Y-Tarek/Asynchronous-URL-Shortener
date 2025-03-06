from .utility import update_clicks, is_rate_limited
from rest_framework.views import View
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework import status
from asgiref.sync import sync_to_async
from .models import ShortenedURL
from .serializers import ShortenURlSerializer


@method_decorator(csrf_exempt, name="dispatch")
class ShortenURLAPI(View):
    """Create URL API"""

    serializer_class = ShortenURlSerializer

    async def post(self, request):
        was_limited = is_rate_limited(request,"POST",'shorten_url')
        if was_limited:
            return JsonResponse(
                {"detail": "Too many attempts. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        data = json.loads(request.body.decode("utf-8"))

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        original_url = data.get("original_url")

             
        cached_shortened = cache.get(original_url)
        if cached_shortened:
            return JsonResponse({"shortened_url": cached_shortened})

        short_url, created = await sync_to_async(ShortenedURL.objects.get_or_create)(
            original_url=original_url
        )
        cache.set(original_url, short_url.shortened_code, timeout=60 * 60)

        return JsonResponse({"shortened_url": short_url.shortened_code})


class ReturnOriginalURLAPI(View):
    """Retrieve Base URL from shorten one"""

    async def get(self, request, shortened_url):
        was_limited = is_rate_limited(request,"GET",'original_url')
        if was_limited:
            return JsonResponse(
                {"detail": "Too many attempts. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        cached_url = cache.get(shortened_url)

        if cached_url:
            update_clicks.delay(shortened_url)
            return JsonResponse({"original_url": cached_url})

        obj = await ShortenedURL.objects.filter(shortened_code=shortened_url).afirst()
        if not obj:
            return JsonResponse({"error": "URL not found"}, status=404)

        cache.set(shortened_url, obj.original_url, timeout=60 * 60)
        update_clicks.delay(shortened_url)

        return JsonResponse({"URL":obj.original_url})


class ReturnStatsAPI(View):
    """Retrieve statstics for the URL"""

    async def get(self, request, shortened_url):
        was_limited = is_rate_limited(request,"GET",'url-stats')
        if was_limited:
            return JsonResponse(
                {"detail": "Too many attempts. Please try again later."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        obj = await ShortenedURL.objects.filter(shortened_code=shortened_url).afirst()
        if not obj:
            return JsonResponse({"error": "URL not found"}, status=404)
        return JsonResponse({"clicks": obj.clicks})
