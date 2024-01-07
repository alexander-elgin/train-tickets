from django.db import models

from carriages.models import Carriage


class Seat(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE, default=None, db_index=True)
    number = models.IntegerField(blank=False, null=False)
    business = models.BooleanField(default=False, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['carriage', 'number'], name='unique_seat_carriage_number')
        ]

    def __str__(self):
        return str(self.carriage.id) + "-" + str(self.number)
