
from django.urls import path
from core.api_views import library_manager
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('customers',library_manager.serve_customer ,name ="cust_api"),
    path('private', library_manager.private_call),
    path("books",library_manager.serve_book,name="book_api"),
    path("rents",library_manager.serve_rent,name="rent_api"),
    path("signup" ,library_manager.signup , name="sign_up"),
    path("obtain_token" ,obtain_auth_token),
    
]