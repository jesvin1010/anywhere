from django.urls import path
from . import views

urlpatterns = [
    # AUTH   
    path('', views.login_user, name='login_user'),      # root → login
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_user, name="logout_user"),
    path('home/', views.home, name='home'),

    # MATCHES FLOW
    path("matches/", views.matches_sports, name="matches_sports"),
    path("matches/sport/<int:sport_id>/", views.competitions_list, name="competitions_list"),
    path("matches/competition/<int:competition_id>/", views.matches_list, name="matches_list"),

    # TEAMS FLOW    
    path("teams/", views.teams_sports, name="teams_sports"),
    path("teams/sport/<int:sport_id>/", views.teams_list, name="teams_list"),
    path("teams/team/<int:team_id>/", views.team_matches, name="team_matches"),

    # PLAYERS FLOW  
    path("players/", views.players_sports, name="players_sports"),
    path("players/sport/<int:sport_id>/", views.players_competitions, name="players_competitions"),
    path("players/sport/<int:sport_id>/<int:competition_id>/", 
         views.players_teams, name="players_teams"),
    path("players/sport/<int:sport_id>/<int:competition_id>/<int:team_id>/",
         views.players_list, name="players_list"),
    path("player/<int:player_id>/", views.player_detail, name="player_detail"),
]
