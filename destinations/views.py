from rest_framework import viewsets

from destinations.models import Destination
from destinations.serializers import DestinationSerializer


# ViewSets define the view behavior.
class ListDestinations(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
