from django.urls import path
from . import views 

urlpatterns=[ 
    path('match/<match_id>',views.match_page,name='match'),
    path('allmatchs',views.allmatchs_page,name='allmatchs'),
    path('tournoi/<tournoi_id>',views.tournoi_page,name='tournoi'),
    path('alltournois',views.alltournois_page,name='alltournois'),
]