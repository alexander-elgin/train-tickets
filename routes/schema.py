from graphene import relay, Boolean, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from destinations.models import Destination
from destinations.schema import DestinationNode
from routes.models import Route
from utils.active import check_active
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateRoute(GrapheneMutation):
    id = Int()
    destination = Field(DestinationNode)
    duration = Int()

    class Arguments:
        destination_id = Int(name="destination", required=True)
        duration = Int(required=True)

    def mutate(self, info, destination_id, duration):
        check_authentication(info)
        check_active(destination_id, Destination, 'destination')

        route = Route(destination_id=destination_id, duration=duration)
        route.save()

        return CreateRoute(id=route.id, destination=route.destination, duration=route.duration)


class DeleteRoute(GrapheneMutation):
    id = Int()
    active = Boolean()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        route = Route.objects.get(pk=id)
        route.active = False
        route.save()

        return DeleteRoute(id=route.id, active=route.active)


class UpdateRoute(GrapheneMutation):
    id = Int()
    destination = Field(DestinationNode)
    duration = Int()

    class Arguments:
        id = Int(required=True)
        destination_id = Int(name="destination")
        duration = Int()

    def mutate(self, info, id, destination_id=None, duration=None):
        check_authentication(info)
        route = Route.objects.get(pk=id)

        if destination_id is not None:
            check_active(destination_id, Destination, 'destination')
            route.destination_id = destination_id
        if duration is not None:
            route.duration = duration

        route.save()

        return UpdateRoute(id=route.id, destination=route.destination, duration=route.duration)


class Mutation(ObjectType):
    create_route = CreateRoute.Field()
    delete_route = DeleteRoute.Field()
    update_route = UpdateRoute.Field()


class RouteNode(DjangoObjectType):
    class Meta:
        model = Route
        filter_fields = ['id', 'active', 'destination']
        use_connection = True


class Query(ObjectType):
    route = relay.Node.Field(RouteNode)
    routes = OrderedDjangoFilterConnectionField(RouteNode, orderBy=List(of_type=String))
