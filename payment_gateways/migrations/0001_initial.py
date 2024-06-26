# Generated by Django 5.0.1 on 2024-01-08 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='paymentgateway',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_payment_gateway_name'),
        ),
    ]
