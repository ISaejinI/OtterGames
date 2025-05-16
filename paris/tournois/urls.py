from django.urls import path
from . import views 

urlpatterns=[ 
    path('match/<match_id>',views.match_page,name='match'),
    path('allmatchs',views.allmatchs_page,name='allmatchs'),
]