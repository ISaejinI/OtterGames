from django.urls import path
from . import views 

urlpatterns=[ 
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profil/', views.userAccount,name='profil'),
    path('signup/', views.signup_page,name='signup'),
    path('rules/', views.rules_page,name='rules'),
    path('leaderboard/', views.leaderboard_page,name='leaderboard'),
    path('', views.home_page, name='home'),
]