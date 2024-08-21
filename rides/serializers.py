from rest_framework import serializers
from rides.models import Ride, User, RideEvent
from datetime import datetime, timedelta
from django.core.validators import EmailValidator

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id_user', 'email', 'password', 'role', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(source='id_rider',read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    today_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = ['id_ride', 'status', 'pickup_latitude', 'pickup_longitude', 
                  'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'rider', 'driver', 'today_ride_events']

    def get_today_ride_events(self, obj):
        # Return only RideEvents from the last 24 hours
        one_day_ago = datetime.now() - timedelta(days=1)
        recent_books = obj.ride_events.filter(created_at__gte=one_day_ago)
        return RideEventSerializer(recent_books, many=True).data


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Invalid email format")]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True,
    )