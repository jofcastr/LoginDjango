from django.contrib import admin
from django.urls import path, include
from tasks import urls as tasks_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(tasks_urls))
]
