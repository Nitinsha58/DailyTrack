from django.contrib import admin
from django.urls import path, include
from dailytrackapp import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls))
]
