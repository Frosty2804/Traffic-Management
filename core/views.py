from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from djoser.serializers import UserCreateSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import VehicleModel
from .serializers import VehicleModelSerializer

from django.http import JsonResponse
import json
class HomeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def home_page(self, request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                road_names = body_data.get('roads', [])

                # Store road names in session
                request.session['roads'] = road_names

                return JsonResponse({'status': 'success', 'roads': road_names})
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        # Handle GET request
        roads = request.session.get('roads', [])
        return render(request, 'core/home.html', {'roads': roads})


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'User created successfully!')
            return redirect('login')  # Redirect to login page after registration
        else:
            return render(request, 'core/register.html', {'errors': serializer.errors})

    def register_page(self, request):
        return render(request, 'core/register.html')


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = Response({
                'refresh': str(refresh),
                'access': access_token,
            }, status=200)
            response.set_cookie(
                key='jwt',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure= False,
            )
            return response
        else:
            return Response({'errors': {'non_field_errors': ['Invalid credentials.']}}, status=401)

    def login_page(self, request):
        return render(request, 'core/login.html')


class SupervisorViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    # GET request to render the supervisor dashboard
    def supervisor_page(self, request):
        return render(request, 'core/supervisor.html')

    # POST request to handle form submission or any data entry
    def post(self, request):
        # Handle the POST logic here
        data = request.data  # Get the POST data from the request

        # Initialize the serializer with the data
        serializer = VehicleModelSerializer(data=data)

        # Validate the data
        if serializer.is_valid():
            # Save the data to the database
            serializer.save()
            # Redirect to the supervisor dashboard after success
            return redirect('/supervisor/dashboard')  # Redirect after successful submission
        else:
            # If the data is invalid, render the form again with errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MapViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def map_page(self, request):
        # Fetch all vehicle entries from the database
        vehicles = list(VehicleModel.objects.all())
        for vehicle in vehicles:
            print(vehicle.start_latitude, vehicle.start_longitude, vehicle.stop_latitude, vehicle.stop_longitude)
        return render(request, 'core/map.html', {'vehicles': vehicles})


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    # POST request to create a new vehicle entry
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return success response with created data
        return Response(serializer.errors, status=400)  # Return errors if invalid data
