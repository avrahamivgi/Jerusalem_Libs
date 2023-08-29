
from django.urls import path
from . import lib_views

urlpatterns = [
    path('',lib_views.home),

]