from graphene import relay, Boolean, Int, List, Mutation as GrapheneMutation, ObjectType, String
from graphene_django import DjangoObjectType

from payment_gateways.models import PaymentGateway
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class CreatePaymentGateway(GrapheneMutation):
    id = Int()
    name = String()

    class Arguments:
        name = String(required=True)

    def mutate(self, info, name):
        check_authentication(info)
        gateway = PaymentGateway(name=name, active=True)
        gateway.save()

        return CreatePaymentGateway(id=gateway.id, name=gateway.name)


class DeletePaymentGateway(GrapheneMutation):
    id = Int()
    active = Boolean()

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        check_authentication(info)
        gateway = PaymentGateway.objects.get(pk=id)
        gateway.active = False
        gateway.save()

        return DeletePaymentGateway(id=gateway.id, active=gateway.active)


class UpdatePaymentGateway(GrapheneMutation):
    id = Int()
    name = String()

    class Arguments:
        id = Int(required=True)
        name = String(required=True)

    def mutate(self, info, id, name):
        check_authentication(info)
        gateway = PaymentGateway.objects.get(pk=id)
        gateway.name = name

        gateway.save()

        return UpdatePaymentGateway(id=gateway.id, name=gateway.name)


class Mutation(ObjectType):
    create_payment_gateway = CreatePaymentGateway.Field()
    delete_payment_gateway = DeletePaymentGateway.Field()
    update_payment_gateway = UpdatePaymentGateway.Field()


class PaymentGatewayNode(DjangoObjectType):
    class Meta:
        model = PaymentGateway
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'active': ['exact'],
        }
        use_connection = True


class Query(ObjectType):
    payment_gateway = relay.Node.Field(PaymentGatewayNode)
    payment_gateways = OrderedDjangoFilterConnectionField(PaymentGatewayNode, orderBy=List(of_type=String))
