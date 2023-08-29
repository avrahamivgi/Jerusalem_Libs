
from django.urls import path
from core.api_views import user
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("books",user.serve_book,name="book_api"),
    path("rents",user.serve_rent,name="rent_api"), 
    path("change_password",user.change_password), 
       
]