from rest_framework import serializers

from destinations.models import Destination


class DestinationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'active', 'name']

    def validate_name(self, value):
        if value is not None and len(value) < 2:
            raise serializers.ValidationError('The name is too short')

        return value
