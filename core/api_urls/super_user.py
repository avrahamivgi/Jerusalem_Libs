
from django.urls import path
from core.api_views import super_user
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('customers',super_user.serve_customer ,name ="cust_api"),
    path('private', super_user.private_call),
    path("books",super_user.serve_book,name="book_api"),
    path("rents",super_user.serve_rent,name="rent_api"),
    path("signup" ,super_user.signup , name="sign_up"),
    path("obtain_token" ,obtain_auth_token),
    
]