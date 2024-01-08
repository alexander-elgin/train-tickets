from graphene import relay, DateTime, Field, Int, List, Mutation as GrapheneMutation, ObjectType, String
from django.db import transaction
from graphene_django import DjangoObjectType

from payment_gateways.models import PaymentGateway
from payment_gateways.schema import PaymentGatewayNode
from payments.models import Payment
from tickets.models import Ticket
from tickets.schema import TicketNode
from utils.active import check_active
from utils.auth import check_authentication
from utils.sorting import OrderedDjangoFilterConnectionField


class BuyTicket(GrapheneMutation):
    id = Int()
    gateway = Field(PaymentGatewayNode)
    ticket = Field(TicketNode)
    date_time = DateTime()

    class Arguments:
        gateway_id = Int(name="payment_gateway", required=True)
        ticket_id = Int(name="ticket", required=True)

    def mutate(self, info, gateway_id, ticket_id):
        check_authentication(info)
        check_active(gateway_id, PaymentGateway, 'payment gateway')

        try:
            with transaction.atomic():
                ticket = Ticket.objects.get(pk=ticket_id)
                ticket.taken = True
                ticket.save()

                payment = Payment(gateway_id=gateway_id, ticket_id=ticket_id)
                payment.save()
        except:
            raise Exception('Unable to buy the ticket')

        return BuyTicket(
            id=payment.id,
            gateway=payment.gateway,
            ticket=payment.ticket,
            date_time=payment.date_time,
        )


class Mutation(ObjectType):
    buy_ticket = BuyTicket.Field()


class PaymentNode(DjangoObjectType):
    class Meta:
        model = Payment
        filter_fields = {
            'date_time': ['date', 'gt', 'gte', 'lt', 'lte', 'range'],
            'gateway': ['exact'],
            'ticket': ['exact'],
        }
        use_connection = True


class Query(ObjectType):
    payment = relay.Node.Field(PaymentNode)
    payments = OrderedDjangoFilterConnectionField(PaymentNode, orderBy=List(of_type=String))
