from django.contrib import admin
from django.urls import path, include
import core

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # djsoer ur
]
