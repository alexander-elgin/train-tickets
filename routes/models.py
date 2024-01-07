from django.db import models

from destinations.models import Destination


class Route(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, default=None, db_index=True)
    duration = models.IntegerField(blank=False, null=False)
    active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.destination.name + " in " + str(self.duration) + " minutes"
