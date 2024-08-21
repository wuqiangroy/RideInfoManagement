from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import connection

from rides.models import User, Ride
from rides.serializers import RideListSerializer, UserLoginSerializer
from rides.permissions import IsAdmin


class RideViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Ride.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        serializer = RideListSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        lat, lon = serializer.validated_data.get('latitude'), serializer.validated_data.get('longitude')
        status, rider_email = serializer.validated_data.get('status'), serializer.validated_data.get('rider_email')
        page = serializer.validated_data.get('page')
        
        query = """
            SELECT r.id_ride, r.status, r.pickup_latitude, r.pickup_longitude, r.dropoff_latitude, r.dropoff_longitude, r.pickup_time, 
                u1.id_user, u1.role, u1.first_name, u1.last_name, u1.email, u1.phone_number,
                u2.id_user, u2.role, u2.first_name, u2.last_name, u2.email, u2.phone_number
            """
        order = " ORDER BY r.pickup_time ASC"
        
        if lat and lon:
            query += f" ,((r.pickup_latitude - {lat}) * (r.pickup_latitude - {lat}) + (r.pickup_longitude - {lon}) * (r.pickup_longitude - {lon})) AS distance"
            order += ", distance ASC"
        
        query += " FROM rides_ride r LEFT JOIN rides_user u1 ON r.id_rider_id = u1.id_user LEFT JOIN rides_user u2 ON r.id_driver_id = u2.id_user"
        
        conditions = []
        if status:
            conditions.append(f"r.status = '{status}'")
        if rider_email:
            conditions.append(f"u1.email = '{rider_email}'")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        count_query = f"SELECT COUNT(1) as count FROM ({query}) AS subquery"
        with connection.cursor() as cursor:
            cursor.execute(count_query)
            total_count = cursor.fetchone()[0]
        
        query += order
        limit = 10
        offset = limit * (page - 1)
        query += f" LIMIT {limit} OFFSET {offset}"

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        in_condition = ",".join([str(i[0]) for i in results])
        event_query = f"SELECT * FROM rides_rideevent re Where re.id_ride_id IN ({in_condition}) AND re.created_at > datetime('now', '-1 day');"
        with connection.cursor() as cursor:
            cursor.execute(event_query)
            events = cursor.fetchall()

        events_mapping = {}
        for e in events:
            if e[0] in events_mapping:
                events_mapping[e[0]].append({'id_ride_event':e[1], 'description':e[2], 'created_at':e[3]})
            else:
                events_mapping[e[0]] = [{'id_ride_event':e[1], 'description':e[2], 'created_at':e[3]}]
        res = [{
            'id_ride': i[0],
            'status': i[1],
            'pickup_latitude': i[2],
            'pickup_longitude': i[3],
            'dropoff_latitude': i[4],
            'dropoff_longitude': i[5],
            'pickup_time': i[6],
            'rider': {
                'id_user': i[7],
                'role': i[8], 
                'first_name': i[9], 
                'last_name': i[10], 
                'email': i[11], 
                'phone_number': i[12]
            },
            "driver": {
                'id_user': i[13],
                'role': i[14], 
                'first_name': i[15], 
                'last_name': i[16], 
                'email': i[17], 
                'phone_number': i[18]
            },
            'today_ride_events': events_mapping[i[0]] if i[0] in events_mapping else []
        } for i in results]

        return Response({
            'total': total_count,
            'next': None if 10 * page > total_count else page+1,
            'prev': None if page == 1 else page-1,
            'results': res,
            })

class LoginView(generics.GenericAPIView):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid() is not True:
            return Response(serializer.errors, status=400)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email, password=password).first()
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)