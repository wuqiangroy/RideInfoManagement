from datetime import timedelta

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

from django.utils import timezone
from django.db.models import F, ExpressionWrapper, FloatField

from rides.models import User, Ride, RideEvent
from rides.serializers import RideListSerializer, UserLoginSerializer, RideSerializer
from rides.permissions import IsAdmin
from rides.exceptions import CustomValidationError


class RideFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains')
    rider_email = django_filters.CharFilter(field_name='id_rider__email', lookup_expr='icontains')

    class Meta:
        model = Ride
        fields = ['status', 'rider_email']


class RidePagination(PageNumberPagination):
    page_size = 10  


class RideViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Ride.objects.select_related().all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = RideSerializer
    pagination_class = RidePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = RideFilter
    ordering_fields = ['pickup_time']

    def get_queryset(self):
        serializer = RideListSerializer(data=self.request.query_params)
        if not serializer.is_valid():
            raise CustomValidationError(400, "invalid input parameters.")

        validated_data = serializer.validated_data
        queryset = super().get_queryset()

        lat = validated_data.get('latitude')
        lon = validated_data.get('longitude')

        # first query
        if lat and lon:
            queryset = queryset.annotate(
                distance=ExpressionWrapper(
                    (F('pickup_latitude') - lat) ** 2 + 
                    (F('pickup_longitude') - lon) ** 2,
                    output_field=FloatField()
                )
            ).order_by('pickup_time', 'distance')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # second query
        page = self.paginate_queryset(queryset)
        if page is not None:
            ride_ids = [ride.id_ride for ride in page]
            # third query
            ride_events = RideEvent.objects.select_related().filter(
                id_ride__in=ride_ids,
                created_at__gt=timezone.now() - timedelta(days=1)
            )

            ride_event_map = {}
            for event in ride_events:
                if event.id_ride in ride_event_map:
                    ride_event_map[event.id_ride].append(event)
                else:
                    ride_event_map[event.id_ride] = [event]

            serializer = self.get_serializer(page, many=True, context={'ride_event_map': ride_event_map})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
            }, status=200)
        return Response({'detail': 'Invalid credentials'}, 401)