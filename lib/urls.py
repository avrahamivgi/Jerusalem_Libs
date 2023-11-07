from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.lib_urls"), name = "render_temp"),
    path("api/v1/", include("core.mega_api_urls")),

]


#images runs only on debug because that this is thing that the cloud needs to handle..
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)