from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from destinations.models import Destination
from destinations.serializers import DestinationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DestinationView(ListAPIView):
    queryset = Destination.objects.all().order_by('name')
    serializer_class = DestinationSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request):
        serializer = DestinationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
