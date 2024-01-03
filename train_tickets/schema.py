import graphene
from graphene_django import DjangoObjectType

from destinations.models import Destination


class DestinationType(DjangoObjectType):
    class Meta:
        model = Destination
        fields = ("id", "name")


class Query(graphene.ObjectType):
    all_destinations = graphene.List(DestinationType)

    def resolve_all_destinations(root, info):
        return Destination.objects.all()


schema = graphene.Schema(query=Query)
