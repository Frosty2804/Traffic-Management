from django.db import models

class VehicleModel(models.Model):
    number_plate = models.CharField(max_length=10, primary_key=True)
    start_latitude = models.FloatField()
    start_longitude = models.FloatField()
    stop_latitude = models.FloatField()
    stop_longitude = models.FloatField()

    def __str__(self):
        return f"Emergency Vehicle {self.number_plate}"

    class Meta:
        verbose_name = "Emergency Vehicle"
        verbose_name_plural = "Emergency Vehicles"
