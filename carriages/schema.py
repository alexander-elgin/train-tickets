from graphene import relay, Boolean, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from carriages.models import Carriage
from trains.models import Train
from trains.schema import TrainNode
from utils.active import check_active
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateCarriage(GrapheneMutation):
    id = Int()
    train = Field(TrainNode)
    sleeping = Boolean()

    class Arguments:
        train_id = Int(name="train", required=True)
        sleeping = Boolean()

    def mutate(self, info, train_id, sleeping):
        check_authentication(info)
        check_active(train_id, Train, 'train')

        carriage = Carriage(train_id=train_id, sleeping=sleeping)
        carriage.save()

        return CreateCarriage(id=carriage.id, train=carriage.train, sleeping=carriage.sleeping)


class DeleteCarriage(GrapheneMutation):
    id = Int()
    active = Boolean()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        carriage = Carriage.objects.get(pk=id)
        carriage.active = False
        carriage.save()

        return DeleteCarriage(id=carriage.id, active=carriage.active)


class UpdateCarriage(GrapheneMutation):
    id = Int()
    train = Field(TrainNode)
    sleeping = Boolean()

    class Arguments:
        id = Int(required=True)
        train_id = Int(name="train")
        sleeping = Boolean()

    def mutate(self, info, id, train_id=None, sleeping=None):
        check_authentication(info)
        carriage = Carriage.objects.get(pk=id)

        if train_id is not None:
            check_active(train_id, Train, 'train')
            carriage.train_id = train_id
        if sleeping is not None:
            carriage.sleeping = sleeping

        carriage.save()

        return UpdateCarriage(id=carriage.id, train=carriage.train, sleeping=carriage.sleeping)


class Mutation(ObjectType):
    create_carriage = CreateCarriage.Field()
    delete_carriage = DeleteCarriage.Field()
    update_carriage = UpdateCarriage.Field()


class CarriageNode(DjangoObjectType):
    class Meta:
        model = Carriage
        filter_fields = ['id', 'active', 'sleeping', 'train']
        use_connection = True


class Query(ObjectType):
    carriage = relay.Node.Field(CarriageNode)
    carriages = OrderedDjangoFilterConnectionField(CarriageNode, orderBy=List(of_type=String))
