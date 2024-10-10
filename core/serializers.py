# serializers.py
from rest_framework import serializers
from .models import VehicleModel

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ['number_plate', 'start_longitude', 'stop_longitude', 'start_latitude', 'stop_latitude']
