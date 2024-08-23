from rest_framework import serializers
from django.core.validators import EmailValidator

from rides.models import RideEvent, User, Ride


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']

class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(source='id_rider')
    driver = UserSerializer(source='id_driver')
    today_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id_ride', 'status', 'pickup_latitude', 'pickup_longitude',
            'dropoff_latitude', 'dropoff_longitude', 'pickup_time',
            'rider', 'driver', 'today_ride_events'
        ]

    def get_today_ride_events(self, obj):
        ride_event_map = self.context.get('ride_event_map', {})
        events = ride_event_map.get(obj.id_ride, [])
        return RideEventSerializer(events, many=True).data




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