from rest_framework.response import Response
from rest_framework.views import APIView

from destinations.models import Destination
from destinations.serializers import DestinationSerializer


class DestinationView(APIView):
    def get(self, request):
        serializer = DestinationSerializer(Destination.objects.all(), many=True)
        return Response(serializer.data)
