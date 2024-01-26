from rest_framework import routers

from destinations.views import ListDestinations


router = routers.DefaultRouter()
router.register('', ListDestinations)
