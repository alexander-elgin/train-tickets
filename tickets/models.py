from django.db import models

from seats.models import Seat
from trips.models import Trip


class Ticket(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, default=None, db_index=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None, db_index=True)
    price = models.FloatField(blank=False, null=False, db_index=True)
    taken = models.BooleanField(default=False, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seat', 'trip'], name='unique_ticket_seat_trip')
        ]

    def __str__(self):
        return str(self.trip) + " " + str(self.seat)
