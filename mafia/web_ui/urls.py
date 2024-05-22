from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="mafia-home"),
    path('create/', views.create_game, name='create_game'),
    path('join/', views.join_game, name='join_game'),
    path('game/<str:game_code>/', views.game_detail, name='game_detail'),
    path('game/<str:game_code>/start/', views.start_game, name='start_game'),
    path('api/game/<str:game_code>/players/', views.get_players, name='get_players'),
    path('api/game/role', views.get_role, name='get_role'),
    path('done/', views.reset, name="reset")
]