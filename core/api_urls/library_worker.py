
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from core.api_views import library_worker
from core.api_views.public import signup


urlpatterns = [
    path('customers',library_worker.serve_customer ,name ="cust_api"),
    path("books",library_worker.serve_book,name="book_api"),
    path("rents",library_worker.serve_rent,name="rent_api"),
    path("obtain_token" ,obtain_auth_token),
    path("signup",signup),
]