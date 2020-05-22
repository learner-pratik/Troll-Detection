from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('infoinsta',views.infoinsta,name='infoinsta'),
    path('inforeddit',views.inforeddit,name='inforeddit'),
    path('infofacebook',views.infofacebook,name='infofacebook'),
    path('infoyoutube',views.infoyoutube,name='infoyoutube'),
    path('infotelegram',views.infotelegram,name='infotelegram'),
    # path('logininsta',views.logininsta,name='logininsta'),
    # path('loginreddit',views.loginreddit,name='loginreddit'),
]