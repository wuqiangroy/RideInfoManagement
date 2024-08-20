from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rides.views import RideViewSet, LoginView

router = DefaultRouter()
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
