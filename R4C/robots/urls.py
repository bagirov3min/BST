from django.urls import path

from R4C import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('add_robot/', views.add_robot, name='add_robot'),
    path('generate_excel/', views.generate_excel, name='generate_excel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)