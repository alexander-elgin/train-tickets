from graphene import relay, Boolean, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from destinations.models import Destination
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateDestination(GrapheneMutation):
    id = String()
    active = Boolean()
    name = String()

    class Arguments:
        id = String(required=True)
        active = Boolean()
        name = String(required=True)

    def mutate(self, info, id, name, active=True):
        check_authentication(info)
        destination = Destination(id=id, name=name, active=active)
        destination.save()

        return CreateDestination(id=destination.id, name=destination.name, active=destination.active)


class DeleteDestination(GrapheneMutation):
    id = String()
    active = Boolean()
    name = String()

    class Arguments:
        id = String(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        destination = Destination.objects.get(pk=id)
        destination.active = False
        destination.save()

        return DeleteDestination(id=destination.id, name=destination.name, active=destination.active)


class UpdateDestination(GrapheneMutation):
    id = String()
    active = Boolean()
    name = String()

    class Arguments:
        id = String(required=True)
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
