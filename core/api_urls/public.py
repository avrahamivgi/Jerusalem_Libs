
from django.urls import path
from rest_framework.authtoken.views import CustomObtainAuthToken
from core.api_views import public


urlpatterns = [
    path("books",public.serve_book,name="book_api"),
    path("signup",public.signup),
    path("obtain_token" ,CustomObtainAuthToken.as_view()),

]