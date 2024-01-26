from django.urls import path

from destinations.views import DestinationView


urlpatterns = [
    path('', DestinationView.as_view())
]
