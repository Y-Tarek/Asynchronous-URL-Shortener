from django.urls import path
from .views import ShortenURLAPI, ReturnOriginalURLAPI, ReturnStatsAPI

urlpatterns = [
    path("url/store/", ShortenURLAPI.as_view(), name="shorten_url"),
    path(
        "url/<str:shortened_url>/", ReturnOriginalURLAPI.as_view(), name="redirect_url"
    ),
    path("url/stats/<str:shortened_url>/", ReturnStatsAPI.as_view(), name="stats"),
]
