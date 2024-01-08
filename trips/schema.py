from graphene import relay, DateTime, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType
from django.utils import timezone

from routes.models import Route
from routes.schema import RouteNode
from trips.models import Trip
from utils.active import check_active
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


def validate_date(date):
    if date < timezone.now():
        raise Exception("The date time is invalid")


class CreateTrip(GrapheneMutation):
    id = Int()
    route = Field(RouteNode)
    date_time = DateTime()

    class Arguments:
        route_id = Int(name="route", required=True)
        date_time = DateTime(required=True)

    def mutate(self, info, route_id, date_time):
        check_authentication(info)
        check_active(route_id, Route, 'route')
        validate_date(date_time)

        trip = Trip(route_id=route_id, date_time=date_time)
        trip.save()

        return CreateTrip(id=trip.id, route=trip.route, date_time=trip.date_time)


class UpdateTrip(GrapheneMutation):
    id = Int()
    route = Field(RouteNode)
    date_time = DateTime()

    class Arguments:
        id = Int(required=True)
        route_id = Int(name="route")
        date_time = DateTime()

    def mutate(self, info, id, route_id=None, date_time=None):
        check_authentication(info)
        trip = Trip.objects.get(pk=id)

        if route_id is not None:
            check_active(route_id, Route, 'route')
            trip.route_id = route_id
        if date_time is not None:
            validate_date(date_time)
            trip.date_time = date_time

        trip.save()

        return UpdateTrip(id=trip.id, route=trip.route, date_time=trip.date_time)


class Mutation(ObjectType):
    create_trip = CreateTrip.Field()
    update_trip = UpdateTrip.Field()


class TripNode(DjangoObjectType):
    class Meta:
        model = Trip
        filter_fields = {
            'date_time': ['date', 'gt', 'gte', 'lt', 'lte', 'range'],
            'route': ['exact'],
        }
        use_connection = True


class Query(ObjectType):
    trip = relay.Node.Field(TripNode)
    trips = OrderedDjangoFilterConnectionField(TripNode, orderBy=List(of_type=String))
