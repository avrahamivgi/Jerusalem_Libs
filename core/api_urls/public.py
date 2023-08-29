
from django.urls import path
from core.api_views import public


urlpatterns = [
    path("books",public.serve_book,name="book_api"),
    path("signup",public.signup)
]