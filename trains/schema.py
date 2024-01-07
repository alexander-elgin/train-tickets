from graphene import relay, Boolean, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from trains.models import Train
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreateTrain(GrapheneMutation):
    id = Int()
    active = Boolean()

    def mutate(self, info):
        check_authentication(info)
        train = Train(active=True)
        train.save()

        return CreateTrain(id=train.id, active=train.active)


class DeleteTrain(GrapheneMutation):
    id = Int()
    active = Boolean()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        train = Train.objects.get(pk=id)
        train.active = False
        train.save()

        return DeleteTrain(id=train.id, active=train.active)


class Mutation(ObjectType):
    create_train = CreateTrain.Field()
    delete_train = DeleteTrain.Field()


class TrainNode(DjangoObjectType):
    class Meta:
        model = Train
        filter_fields = ['id', 'active']
        use_connection = True


class Query(ObjectType):
    train = relay.Node.Field(TrainNode)
    trains = OrderedDjangoFilterConnectionField(TrainNode, orderBy=List(of_type=String))
