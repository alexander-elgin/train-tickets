from graphene import relay, DateTime, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType
from django.utils import timezone

from destinations.schema import DestinationNode
from trips.models import Trip
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


def validate_date(date, min_date, date_type):
    if date < min_date:
        raise Exception(f"The {date_type} date is invalid")


class CreateTrip(GrapheneMutation):
    id = Int()
    destination = Field(DestinationNode)
    departure_date_time = DateTime()
    arrival_date_time = DateTime()

    class Arguments:
        destination_id = Int(name="destination", required=True)
        departure_date_time = DateTime(required=True)
        arrival_date_time = DateTime(required=True)

    def mutate(self, info, destination_id, departure_date_time, arrival_date_time):
        check_authentication(info)
        validate_date(departure_date_time, timezone.now(), "departure")
        validate_date(arrival_date_time, departure_date_time, "arrival")

        trip = Trip(
            destination_id=destination_id,
            departure_date_time=departure_date_time,
            arrival_date_time=arrival_date_time
        )
        trip.save()

        return CreateTrip(
            id=trip.id,
            destination=trip.destination,
            departure_date_time=trip.departure_date_time,
            arrival_date_time=trip.arrival_date_time
        )


class UpdateTrip(GrapheneMutation):
    id = Int()
    destination = Field(DestinationNode)
    departure_date_time = DateTime()
    arrival_date_time = DateTime()

    class Arguments:
        id = Int(required=True)
        destination_id = Int(name="destination")
        departure_date_time = DateTime()
        arrival_date_time = DateTime()

    def mutate(self, info, id, destination_id=None, departure_date_time=None, arrival_date_time=None):
        check_authentication(info)
        trip = Trip.objects.get(pk=id)

        if destination_id is not None:
            trip.destination_id = destination_id
        if departure_date_time is not None:
            validate_date(departure_date_time, timezone.now(), "departure")
            trip.departure_date_time = departure_date_time
        if arrival_date_time is not None:
            validate_date(arrival_date_time, trip.departure_date_time, "arrival")
            trip.arrival_date_time = arrival_date_time

        trip.save()

        return UpdateTrip(
            id=trip.id,
            destination=trip.destination,
            departure_date_time=trip.departure_date_time,
            arrival_date_time=trip.arrival_date_time
        )


class Mutation(ObjectType):
    create_trip = CreateTrip.Field()
    update_trip = UpdateTrip.Field()


class TripNode(DjangoObjectType):
    class Meta:
        model = Trip
        filter_fields = {
            'arrival_date_time': ['date', 'gt', 'gte', 'lt', 'lte', 'range'],
            'departure_date_time': ['date', 'gt', 'gte', 'lt', 'lte', 'range'],
            'destination': ['exact'],
        }
        use_connection = True


class Query(ObjectType):
    trip = relay.Node.Field(TripNode)
    trips = OrderedDjangoFilterConnectionField(TripNode, orderBy=List(of_type=String))
