from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, SupervisorViewSet, HomeViewSet, MapViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'auth/api/register', RegisterViewSet, basename='register-api')
router.register(r'auth/api/login', LoginViewSet, basename='login-api')
router.register(r'api/vehicles', VehicleViewSet, basename='vehicle-api')

urlpatterns = [
    # Redirect root URL to /home
    path('', RedirectView.as_view(url='/home/', permanent=True)),

    # API endpoints
    path('', include(router.urls)),

    # Home page
    path('home/', HomeViewSet.as_view({'post': 'home_page', 'get': 'home_page'}), name='home'),
    # path('home/', HomeViewSet.as_view({'get': 'home_page'}), name='home'),

    # Djoser JWT authentication URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('auth/register/', RegisterViewSet.as_view({'get': 'register_page', 'post': 'create'}), name='register'),
    path('auth/login/', LoginViewSet.as_view({'get': 'login_page', 'post': 'create'}), name='login'),

    path('supervisor/dashboard/', SupervisorViewSet.as_view({'get': 'supervisor_page'}), name='supervisor'),
    path('supervisor/dashboard/map', MapViewSet.as_view({'get': 'map_page'}), name='map'),
]
