from django.db import models

from destinations.models import Destination


class Trip(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    destination = models.ForeignKey(Destination, blank=False, null=False, on_delete=models.DO_NOTHING)
    departure_date_time = models.DateTimeField(blank=False, null=False)
    arrival_date_time = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.id
