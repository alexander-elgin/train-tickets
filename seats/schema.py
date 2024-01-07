from graphene import relay, Boolean, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from carriages.schema import CarriageNode
from seats.models import Seat
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


def validate_number(number):
    if number <= 0:
        raise Exception("The number is invalid")


class CreateSeat(GrapheneMutation):
    id = Int()
    carriage = Field(CarriageNode)
    number = Int()
    business = Boolean()

    class Arguments:
        carriage_id = Int(name="carriage", required=True)
        number = Int(required=True)
        business = Boolean()

    def mutate(self, info, carriage_id, number, business=False):
        check_authentication(info)
        validate_number(number)

        seat = Seat(carriage_id=carriage_id, number=number, business=business)
        seat.save()

        return CreateSeat(id=seat.id, carriage=seat.carriage, number=seat.number, business=seat.business)


class UpdateSeat(GrapheneMutation):
    id = Int()
    carriage = Field(CarriageNode)
    number = Int()
    business = Boolean()

    class Arguments:
        id = Int(required=True)
        carriage_id = Int(name="carriage", required=True)
        number = Int(required=True)
        business = Boolean()

    def mutate(self, info, id, carriage_id=None, number=None, business=None):
        check_authentication(info)
        seat = Seat.objects.get(pk=id)

        if business is not None:
            seat.business = business
        if carriage_id is not None:
            seat.carriage_id = carriage_id
        if number is not None:
            validate_number(number)
            seat.number = number

        seat.save()

        return UpdateSeat(id=seat.id, carriage=seat.carriage, number=seat.number, business=seat.business)


class Mutation(ObjectType):
    create_seat = CreateSeat.Field()
    update_seat = UpdateSeat.Field()


class SeatNode(DjangoObjectType):
    class Meta:
        model = Seat
        filter_fields = ['id', 'business', 'carriage']
        use_connection = True


class Query(ObjectType):
    seat = relay.Node.Field(SeatNode)
    seats = OrderedDjangoFilterConnectionField(SeatNode, orderBy=List(of_type=String))
