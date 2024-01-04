from graphene import relay, List, ObjectType, String
from graphene_django import DjangoObjectType

from destinations.models import Destination
from utils.sorting import OrderedDjangoFilterConnectionField


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
    destinations = OrderedDjangoFilterConnectionField(DestinationNode, orderBy=List(of_type=String))
