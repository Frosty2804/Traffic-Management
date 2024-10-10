from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import os
from django.shortcuts import redirect, render
from django.views.generic import View
from djoser.serializers import UserCreateSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import VehicleModel
from .serializers import VehicleModelSerializer
import subprocess


class HomeViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def home_page(self, request):
        return render(request, 'core/home.html')


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

    # PUT request to update an existing vehicle entry

class ExecuteScriptView(View):
    def post(self, request):
        script_path = 'scanner/app.py'  # Adjust to the correct script location

        # Ensure the script path is safe and exists
        if not os.path.exists(script_path):
            return JsonResponse({'error': 'Script not found.'}, status=404)

        try:
            # Run the script in a subprocess
            process = subprocess.Popen(['python3', script_path])

            # Set the redirect URL to localhost:5000
            return JsonResponse({
                'message': 'Script is being executed.',
                'pid': process.pid,
                'redirect_url': 'http://127.0.0.1:5000/'  # Redirect to localhost:5000
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': 'Failed to execute script.', 'details': str(e)}, status=500)
