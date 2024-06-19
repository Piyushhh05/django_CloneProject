from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('client_registration',client_registration,name='client_registration'),
    path('client_login',client_login,name='client_login'),
    path('client_logout',client_logout,name='client_logout'),
    path('display<type>',client_menu,name='client_menu'),
    path('addtocart',addtocart,name='addtocart'),
    path('cart',cart,name='cart'),
    path('changepassword',changepassword,name='changepassword'),
    path('otp',otp,name='otp'),
    path('forgotpassword/',forgotpassword,name='forgotpassword'),
    path('updatepassword/',updatepassword,name='updatepassword'),
    path('forgotpasswordotp/',forgotpasswordotp,name='forgotpasswordotp'),
    path('Buy',Buy,name='Buy')
    ]