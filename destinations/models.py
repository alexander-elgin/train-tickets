from django.db import models


class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100, null=False, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_destination_name')
        ]

    def __str__(self):
        return self.name
