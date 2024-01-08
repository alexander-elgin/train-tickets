from graphene import relay, Boolean, Field, Float, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from seats.schema import SeatNode
from trips.schema import TripNode
from tickets.models import Ticket
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


def validate_price(price):
    if price < 0:
        raise Exception("The price is invalid")


class CreateTicket(GrapheneMutation):
    id = Int()
    seat = Field(SeatNode)
    trip = Field(TripNode)
    price = Float()
    taken = Boolean()

    class Arguments:
        seat_id = Int(name="seat", required=True)
        trip_id = Int(name="trip", required=True)
        price = Float(required=True)

    def mutate(self, info, seat_id, trip_id, price):
        check_authentication(info)
        validate_price(trip_id)

        ticket = Ticket(seat_id=seat_id, trip_id=trip_id, price=price)
        ticket.save()

        return CreateTicket(id=ticket.id, seat=ticket.seat, trip=ticket.trip, price=ticket.price, taken=ticket.taken)


class UpdateTicket(GrapheneMutation):
    id = Int()
    seat = Field(SeatNode)
    trip = Field(TripNode)
    price = Float()
    taken = Boolean()

    class Arguments:
        id = Int(required=True)
        price = Float(required=True)

    def mutate(self, info, id, price):
        check_authentication(info)
        ticket = Ticket.objects.get(pk=id)

        if ticket.taken:
            raise Exception("The ticket is taken already")

        validate_price(price)
        ticket.price = price

        ticket.save()

        return UpdateTicket(id=ticket.id, seat=ticket.seat, trip=ticket.trip, price=ticket.price, taken=ticket.taken)


class Mutation(ObjectType):
    create_ticket = CreateTicket.Field()
    update_ticket = UpdateTicket.Field()


class TicketNode(DjangoObjectType):
    class Meta:
        model = Ticket
        filter_fields = {
            'id': ['exact'],
            'seat': ['exact'],
            'trip': ['exact'],
            'taken': ['exact'],
            'price': ['lt', 'lte'],
        }
        use_connection = True


class Query(ObjectType):
    ticket = relay.Node.Field(TicketNode)
    tickets = OrderedDjangoFilterConnectionField(TicketNode, orderBy=List(of_type=String))
