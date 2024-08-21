from django.db import migrations
from django.utils import timezone
import random

def create_initial_data(apps, schema_editor):
    User = apps.get_model('rides', 'User')
    Ride = apps.get_model('rides', 'Ride')
    RideEvent = apps.get_model('rides', 'RideEvent')

    User.objects.create(
        id_user=1,
        role='admin',
        first_name='Admin',
        last_name='User',
        email='admin@example.com',
        phone_number='1234567890',
        password="adminpassword" 
    )

    for i in range(2, 102):
        User.objects.create(
            id_user=i,
            role='user',
            first_name=f'User{i}',
            last_name='',
            email=f'user{i}@example.com',
            phone_number='1234567890',
            password="adminpassword" 
        )

    for i in range(1, 1001):
        ride = Ride.objects.create(
            id_ride=i,
            status=random.choice(["en-route", "pickup", "dropoff"]),
            id_rider=User.objects.get(id_user=i % 100 + 1),  
            id_driver=User.objects.get(id_user=(i + 1) % 100 + 1),  
            pickup_latitude=40.0 + (i % 10) * 0.01,
            pickup_longitude=-75.0 + (i % 10) * 0.01,
            dropoff_latitude=40.1 + (i % 10) * 0.01,
            dropoff_longitude=-75.1 + (i % 10) * 0.01,
            pickup_time=timezone.now()
        )

        for j in range(1, 6): 
            RideEvent.objects.create(
                id_ride_event=(i - 1) * 5 + j,
                id_ride=ride,
                description=f'Event {j} for Ride {i}',
                created_at=timezone.now()
            )

class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0001_initial'),  
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
