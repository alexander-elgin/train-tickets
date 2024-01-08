from django.db import models

from payment_gateways.models import PaymentGateway
from tickets.models import Ticket


class Payment(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE, default=None, db_index=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, default=None, db_index=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ticket'], name='unique_payment_ticket')
        ]

    def __str__(self):
        return str(self.ticket)
