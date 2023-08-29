
from django.urls import path , include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("public/",include("core.api_urls.public")),
    path("user/",include("core.api_urls.user")),
    path("lib_worker/" ,include("core.api_urls.library_worker")),
    path("lib_manager/" , include("core.api_urls.library_manager")),
    path("super_user/", include('core.api_urls.super_user')),
]