from django.contrib import admin

from payment_gateways.models import PaymentGateway

admin.site.register(PaymentGateway)
