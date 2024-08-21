from rest_framework import serializers
from django.core.validators import EmailValidator


class RideListSerializer(serializers.Serializer):
    status = serializers.ChoiceField(required=False, choices=["en-route", "pickup", "dropoff"])
    rider_email = serializers.EmailField(required=False, validators=[EmailValidator(message="Invalid email format")])
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    page = serializers.IntegerField(required=False, default=1)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Invalid email format")]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True,
    )