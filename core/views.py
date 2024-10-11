from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from djoser.serializers import UserCreateSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import VehicleModel
from .serializers import VehicleModelSerializer
import os
import subprocess

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
            return redirect('login')
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
                secure=False,
            )
            return response
        else:
            return Response({'errors': {'non_field_errors': ['Invalid credentials.']}}, status=401)

    def login_page(self, request):
        return render(request, 'core/login.html')


class SupervisorViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Ensure only authenticated users can access

    def supervisor_page(self, request):
        return render(request, 'core/supervisor.html')

    def create(self, request):
        serializer = VehicleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)  # Return success response with created data
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MapViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def map_page(self, request):
        vehicles = VehicleModel.objects.all()
        return render(request, 'core/map.html', {'vehicles': vehicles})


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    permission_classes = [AllowAny]



class ExecuteScriptView(View):
    def post(self, request):
        script_path = 'scanner/app.py'

        if not os.path.exists(script_path):
            return JsonResponse({'error': 'Script not found.'}, status=404)

        try:
            process = subprocess.Popen(['python', script_path])
            return JsonResponse({
                'message': 'Script is being executed.',
                'pid': process.pid,
                'redirect_url': 'http://127.0.0.1:5000/'
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': 'Failed to execute script.', 'details': str(e)}, status=500)
