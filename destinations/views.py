from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from destinations.models import Destination
from destinations.serializers import DestinationSerializer


class DestinationView(APIView):
    def get(self, request):
        serializer = DestinationSerializer(Destination.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
