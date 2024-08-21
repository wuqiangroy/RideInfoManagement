import math
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Cast

from rides.models import Ride, User
from rides.serializers import RideSerializer
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

    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    pagination_class = RidePagination
    # permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = RideFilter
    ordering_fields = ['pickup_time']  
    
    def get_queryset(self):
        queryset = Ride.objects.all()
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')
        try:
            if lat and lon:
                queryset = queryset.annotate(
                    distance=ExpressionWrapper(
                    (F('pickup_latitude') - float(lat)) ** 2 + (F('pickup_longitude') - float(lon)) ** 2,
                    output_field=FloatField()
                    )
                ).order_by('pickup_time', 'distance')
            return queryset
        except (ValueError, TypeError):
            raise CustomValidationError(message="Latitude and longitude must be valid float numbers.")


class LoginView(generics.GenericAPIView):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
