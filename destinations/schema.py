from graphene import relay, Boolean, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from destinations.models import Destination
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateDestination(GrapheneMutation):
    id = Int()
    name = String()

    class Arguments:
        name = String(required=True)

    def mutate(self, info, name):
        check_authentication(info)
        destination = Destination(name=name, active=True)
        destination.save()

        return CreateDestination(id=destination.id, name=destination.name)


class DeleteDestination(GrapheneMutation):
    id = Int()
    active = Boolean()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        destination = Destination.objects.get(pk=id)
        destination.active = False
        destination.save()

        return DeleteDestination(id=destination.id, active=destination.active)


class UpdateDestination(GrapheneMutation):
    id = Int()
    name = String()

    class Arguments:
        id = Int(required=True)
        name = String(required=True)

    def mutate(self, info, id, name):
        check_authentication(info)
        destination = Destination.objects.get(pk=id)
        destination.name = name

        destination.save()

        return UpdateDestination(id=destination.id, name=destination.name)


class Mutation(ObjectType):
    create_destination = CreateDestination.Field()
    delete_destination = DeleteDestination.Field()
    update_destination = UpdateDestination.Field()


class DestinationNode(DjangoObjectType):
    class Meta:
        model = Destination
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'active': ['exact'],
        }
        use_connection = True


class Query(ObjectType):
    destination = relay.Node.Field(DestinationNode)
    destinations = OrderedDjangoFilterConnectionField(DestinationNode, orderBy=List(of_type=String))
