from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_info/', views.get_info, name='get_info'),
    path('insert_data/', views.insert_data, name='inser_data'),
    path('insert_rent_desc/', views.store_rent_desc, name='insert_rent_info'),
    path('insert_rent_data/', views.store_rent_data, name='insert_rent_data'),
    path('convert/', views.convert, name='convert'),
    path('info/', views.get_currency, name='info'),
    path('compare/', views.compare, name='compare'),
    path('latestValues/', views.get_latest, name='latest'),
    # path('compareImg/', views.compare_img, name='compareImg'),
    path('compareImg2/<str:from_cur>/<str:to_cur>', views.base_64_compare, name='compareImg3'),
    path('dates/', views.get_all_dates, name='allDates'),
    path('compareMult/', views.multiple_compare, name='compare_mult'),
    path('comparMultMobil/<str:base>/<str:others>', views.compare_mult_cur, name='compare_mult_mobil'),
    path('lazy/', views.get_latest_lazy, name='lazy'),
    path('all_rents/', views.get_all_rent_data, name='all_rents'),
    path('rents_ids/', views.get_rent_ids, name='all_rents'),
    path('one_rent/<str:name>', views.one_rent, name='one_rent'),
    path('date_range/', views.get_date_range, name='date_range'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
