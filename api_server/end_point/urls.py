from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_info/', views.get_info, name='get_info'),
    path('insert_data/', views.insert_data, name='inser_data'),
    path('convert/', views.convert, name='convert'),
    path('info/', views.get_currency, name='info'),
    path('compare/', views.compare, name='compare'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)