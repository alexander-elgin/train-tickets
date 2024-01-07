from django.db import models

from routes.models import Route


class Trip(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default=None, db_index=True)
    date_time = models.DateTimeField(blank=False, null=False, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['route', 'date_time'], name='unique_trip_route_date_time')
        ]

    def __str__(self):
        return self.route.destination.name + " " + str(self.date_time)
