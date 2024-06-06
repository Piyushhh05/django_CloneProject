from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('client_registration',client_registration,name='client_registration'),
    path('client_login',client_login,name='client_login'),
    path('client_logout',client_logout,name='client_logout'),
    ]