# RideInfoManagement

This project is ride information management.

## Architecture

### Project Layout

```
RideInfoManagement/
│
├── rim/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── rides/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py  
│   ├── views.py
│   ├── urls.py         
│   └── tests.py
│
├── manage.py
└── db.sqlite3

```

## API Doc

### User login in

- URL: `api/v1/login/`
- Method: `POST`

**Request Body**

```json
{
    "email": "", // string
    "password": "" // string
}
```

**Example**

`curl --location '127.0.0.1:8000/api/v1/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@example.com",
    "password": "adminpassword1"
}'`

**Response**

- Success
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDI5NTMzNSwiaWF0IjoxNzI0MjA4OTM1LCJqdGkiOiI3NTgwNDdlMzFmYjM0OTlmODM4MTVkY2UxOTkzNDZjZSIsImlkX3VzZXIiOjF9.GTX7NRldFhnMxpzeSfBA_gN1UgvBmWBjhhYaRdJGOjU",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0MjA5MjM1LCJpYXQiOjE3MjQyMDg5MzUsImp0aSI6IjViOTg4NDVlZTc5ZjQ0MWFhNmJlZWNiY2IxN2UxZjFmIiwiaWRfdXNlciI6MX0.g1ihu-zHPrs2LG_rYMqJG7jXRtrVcYwt5nxVnbrG9Qw"
}
```
- Failed
```json
{
    "detail": "Invalid credentials"
}
```

### Get all the rides info

- URL: `api/v1/rides/`
- Method: `GET`

**Request Params**
- status  
- rider_email
- latitude
- longitude

`127.0.0.1:8000/api/v1/rides/?status=dropoff&latitude=40.01&longitude=200`

**Authentication**

- --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0MjA4ODQ4LCJpYXQiOjE3MjQyMDg1NDgsImp0aSI6ImIzYTIwOTZiNjBhOTQ0Y2FiOGVjMjUwNjY3MTI4MDFjIiwiaWRfdXNlciI6MX0.Igb9YYhX20PNEVGpIRqakhjrSThiQNackf2yeFCwLUk'    

**Example**:   
`curl --location '127.0.0.1:8000/api/v1/rides/?status=dropoff&latitude=40.01&longitude=200' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0MjA4ODQ4LCJpYXQiOjE3MjQyMDg1NDgsImp0aSI6ImIzYTIwOTZiNjBhOTQ0Y2FiOGVjMjUwNjY3MTI4MDFjIiwiaWRfdXNlciI6MX0.Igb9YYhX20PNEVGpIRqakhjrSThiQNackf2yeFCwLUk'`

**Response**
- Success
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id_ride": 4,
            "status": "dropoff",
            "pickup_latitude": 40.04,
            "pickup_longitude": -74.96,
            "dropoff_latitude": 40.14,
            "dropoff_longitude": -75.05999999999999,
            "pickup_time": "2024-08-21 02:48:33",
            "rider": {
                "id_user": 5,
                "email": "user5@example.com",
                "role": "user",
                "first_name": "User5",
                "last_name": "",
                "phone_number": "1234567890"
            },
            "driver": {
                "id_user": 6,
                "email": "user6@example.com",
                "role": "user",
                "first_name": "User6",
                "last_name": "",
                "phone_number": "1234567890"
            },
            "today_ride_events": [
                {
                    "id_ride_event": 16,
                    "description": "Event 1 for Ride 4",
                    "created_at": "2024-08-21 02:48:33"
                },
                {
                    "id_ride_event": 17,
                    "description": "Event 2 for Ride 4",
                    "created_at": "2024-08-21 02:48:33"
                },
                {
                    "id_ride_event": 18,
                    "description": "Event 3 for Ride 4",
                    "created_at": "2024-08-21 02:48:33"
                },
                {
                    "id_ride_event": 19,
                    "description": "Event 4 for Ride 4",
                    "created_at": "2024-08-21 02:48:33"
                },
                {
                    "id_ride_event": 20,
                    "description": "Event 5 for Ride 4",
                    "created_at": "2024-08-21 02:48:33"
                }
            ]
        }
    ]
}
```

- Failed
```json
{
    "detail": "Authentication credentials were not provided."
}
```
## Run 

- Create a local python env for this project: `python -m venv env`
- Active the env by: `source env/bin/activate` on MacOS/Linux else `.\env\Scripts\activate` on Windows.
- Install the dependencies: `pip install -r requirements.txt`
- Database migrations: `python manage.py migrate`
- Start server: `python manage.py runserver`

If you see the message bellow, means you start the server success.
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 21, 2024 - 06:03:47
Django version 5.1, using settings 'rim.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```