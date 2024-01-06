from django.db import models

from destinations.models import Destination


class Trip(models.Model):
    id = models.IntegerField(primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, default=None)
    departure_date_time = models.DateTimeField(blank=False, null=False)
    arrival_date_time = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.destination.name + " " + str(self.departure_date_time)
