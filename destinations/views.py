from rest_framework.decorators import api_view
from rest_framework.response import Response

from destinations.models import Destination
from destinations.serializers import DestinationSerializer


@api_view(['GET'])
def list_destinations(request):
    serializer = DestinationSerializer(Destination.objects.all(), many=True)
    return Response(serializer.data)
