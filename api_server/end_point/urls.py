from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_info/', views.get_info, name='get_info'),
    path('insert_data/', views.insert_data, name='inser_data'),
    path('convert/', views.convert, name='convert'),
    path('info/', views.get_currency, name='info'),
    path('compare/', views.compare, name='compare'),
    path('latestValues/', views.get_latest, name='latest'),
    path('compareImg/', views.compare_img, name='compareImg'),
    path('compareImg/<str:from_cur>/<str:to_cur>', views.compare_img2, name='compareImg2'),
    path('compareImg2/<str:from_cur>/<str:to_cur>', views.base_64_compare, name='compareImg3'),
    path('login/', views.login_view, name='redirect_login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup_view, name="signup"),
    path('dates/',views.get_all_dates,name='allDates'),
    path('compareMult/',views.multiple_compare,name='compare_mult'),
    path('comparMultMobil/<str:base>/<str:others>',views.compare_mult_cur,name='compare_mult_mobil'),
    path('lazy/',views.get_latest_lazy,name='lazy')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)