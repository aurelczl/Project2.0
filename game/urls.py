from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('play/', views.play_view, name='play_view'),
    path('save/', views.save_score, name='save_score'),
    path('list/', views.get_scores, name='get_scores'),
    path('player/', views.player_info, name='player_info'),
    path('launch/', views.launch_game, name='launch_game'),

    path("create/", views.create_player, name="create_player"),
    path("profile/", views.player_profile, name="player_profile"),
    path("delete/", views.delete_player, name="delete_player"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
