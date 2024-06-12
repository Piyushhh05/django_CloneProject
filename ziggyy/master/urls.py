from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('master_registration',master_registration,name='master_registration'),
    path('master_login',master_login,name='master_login'),
    path('master_items',master_items, name='master_items'),
    path('menu',menu,name='menu'),
    path('update/<int:pk>/',update_item,name='update_item'),
    path('delete/<int:pk>/',delete_item,name='delete_item'),

    ]