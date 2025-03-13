from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from config import settings
from config.settings import MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Api/', include('api.urls'), name='shops'),

] + static(MEDIA_URL, document_root=settings.MEDIA_ROOT)