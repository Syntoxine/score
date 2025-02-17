from django.urls import path

from . import views

app_name = 'scoreboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('s/<str:score_name>/', views.score, name='score'),
    path('p/<str:player_name>/', views.player, name='player'),
]
