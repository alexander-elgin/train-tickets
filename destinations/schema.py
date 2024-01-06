from graphene import relay, Boolean, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from destinations.models import Destination
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateDestination(GrapheneMutation):
    active = Boolean()
    name = String()

    class Arguments:
        active = Boolean()
        name = String(required=True)

    def mutate(self, info, name, active=True):
        check_authentication(info)
        destination = Destination(name=name, active=active)
        destination.save()

        return CreateDestination(name=destination.name, active=destination.active)


class DeleteDestination(GrapheneMutation):
    id = Int()
    active = Boolean()
    name = String()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        destination = Destination.objects.get(pk=id)
        destination.active = False
        destination.save()

        return DeleteDestination(id=destination.id, name=destination.name, active=destination.active)


class UpdateDestination(GrapheneMutation):
    id = Int()
    active = Boolean()
    name = String()

    class Arguments:
        id = Int(required=True)
        active = Boolean()
        name = String()

    def mutate(self, info, id, name="", active=True):
        check_authentication(info)
        destination = Destination.objects.get(pk=id)

        if active is not None:
            destination.active = active
        if name != "":
            destination.name = name

        destination.save()

        return UpdateDestination(id=destination.id, name=destination.name, active=destination.active)


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
