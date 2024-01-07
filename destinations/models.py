from django.db import models


class Destination(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    name = models.CharField(max_length=100, null=False, unique=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_destination_name')
        ]

    def __str__(self):
        return self.name
