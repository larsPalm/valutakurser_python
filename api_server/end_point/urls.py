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
    path('latestValues/', views.get_latest, name='latest'),
    path('login/', views.login_view, name='redirect_login'),
    path('signup/', views.signup_view, name="signup"),
    path('compareImg/', views.compare_img, name='compareImg'),
    path('compareImg/<str:from_cur>/<str:to_cur>', views.compare_img2, name='compareImg2'),
    path('compareImg2/<str:from_cur>/<str:to_cur>', views.base_64_compare, name='compareImg3'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)