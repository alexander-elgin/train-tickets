from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from destinations.models import Destination


class DestinationNode(DjangoObjectType):
    class Meta:
        model = Destination
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'active': ['exact'],
        }
        interfaces = (relay.Node,)


class Query(ObjectType):
    destination = relay.Node.Field(DestinationNode)
    destinations = DjangoFilterConnectionField(DestinationNode)
