from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.network),
#   path('admin/', admin.site.urls),
# 	path('build/', views.addr_upload_view),
#   path('net', views.searchpage)
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.JS_URL, document_root=settings.JS_ROOT)
