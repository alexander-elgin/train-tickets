# Generated by Django 5.0.1 on 2024-01-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0005_destination_unique_destination_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='destination',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]
