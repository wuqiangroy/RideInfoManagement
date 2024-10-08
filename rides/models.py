from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Ride(models.Model):
    id_ride = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=64)  # en-route/pickup/dropoff
    id_rider = models.ForeignKey('User', related_name='rider', on_delete=models.CASCADE)
    id_driver = models.ForeignKey('User', related_name='driver', on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id_ride}"

    class Meta:
        app_label = 'rides'


class User(AbstractBaseUser):
    id_user = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=64)  # admin or others
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"User {self.email}"

    class Meta:
        app_label = 'rides'


class RideEvent(models.Model):
    id_ride_event = models.IntegerField(primary_key=True)
    id_ride = models.ForeignKey(Ride, related_name='ride_events', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"RideEvent {self.id_ride_event}"

    class Meta:
        app_label = 'rides'
