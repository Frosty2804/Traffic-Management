# core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class JwtCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ensure that the request has a matched view
        if request.resolver_match:
            view_class = request.resolver_match.func.view_class

            # Check if the view has IsAuthenticated as a permission class
            if issubclass(view_class, APIView):
                permission_classes = getattr(view_class, 'permission_classes', [])
                if IsAuthenticated in permission_classes:
                    jwt_token = request.COOKIES.get('jwt')
                    if jwt_token:
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {jwt_token}'
