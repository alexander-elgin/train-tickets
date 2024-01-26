from django.urls import path

from destinations.views import list_destinations


urlpatterns = [
    path('', list_destinations)
]
