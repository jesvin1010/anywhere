from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Sport, Competition, Team, Player, Match

# auth
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ============================
# 🔹 SIGNUP
# ============================
def signup(request):
    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first,
            last_name=last
        )
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect("login_user")

    return render(request, "polls/signup.html")


# ============================
# 🔹 LOGIN
# ============================
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # go to home after login
        else:
            return render(request, "polls/login.html", {"error": "Invalid credentials"})

    return render(request, "polls/login.html")


# ============================
# 🔹 LOGOUT
# ============================
def logout_user(request):
    logout(request)
    return redirect("login_user")


# ============================
# 🔹 HOME PAGE
# ============================
#mongo used
@login_required
def home(request):
    from .mongo import log_activity  # import inside view

    log_activity(
        user=request.user.username,
        action="Visited Home Page",
        details="User opened the main home page"
    )

    return render(request, "polls/home.html")



# ============================
# 🔹 MATCHES FLOW
# ============================
@login_required(login_url='/')
def matches_sports(request):
    sports = Sport.objects.all()
    return render(request, "polls/matches_sports.html", {"sports": sports})

#mongo used
@login_required(login_url='/')
def competitions_list(request, sport_id):
    from .mongo import log_activity

    sport = Sport.objects.get(sport_id=sport_id)
    competitions = Competition.objects.filter(sport__sport_id=sport_id)

    log_activity(
        user=request.user.username,
        action="Viewed Competitions",
        details={"sport_id": sport_id, "sport_name": sport.name}
    )

    return render(request, "polls/competitions_list.html", {
        "sport": sport,
        "competitions": competitions,
    })



@login_required(login_url='/')
def matches_list(request, competition_id):
    competition = Competition.objects.get(competition_id=competition_id)
    matches = Match.objects.filter(competition__competition_id=competition_id)
    return render(request, "polls/matches_list.html", {
        "competition": competition,
        "matches": matches,
    })


# ============================
# 🔹 TEAMS FLOW
# ============================
@login_required(login_url='/')
def teams_sports(request):
    sports = Sport.objects.all()
    return render(request, "polls/teams_sports.html", {"sports": sports})


@login_required(login_url='/')
def teams_list(request, sport_id):
    sport = Sport.objects.get(sport_id=sport_id)
    competitions = Competition.objects.filter(sport_id=sport_id)
    teams = Team.objects.filter(competition__sport_id=sport_id)
    return render(request, "polls/teams_list.html", {
        "sport": sport,
        "teams": teams,
        "competitions": competitions,
    })


@login_required(login_url='/')
def team_matches(request, team_id):
    team = Team.objects.get(team_id=team_id)
    matches = Match.objects.filter(home_team__team_id=team_id) | \
              Match.objects.filter(away_team__team_id=team_id)
    return render(request, "polls/team_matches.html", {
        "team": team,
        "matches": matches,
    })


# =====================================================
# ⭐⭐⭐ PLAYERS FLOW (NEWLY ADDED) ⭐⭐⭐
# =====================================================

# 1️⃣ List of Sports for Players
@login_required(login_url='/')
def players_sports(request):
    sports = Sport.objects.all()
    return render(request, "polls/players_sports.html", {"sports": sports})


# 2️⃣ Competitions inside a Sport
@login_required(login_url='/')
def players_competitions(request, sport_id):
    sport = get_object_or_404(Sport, sport_id=sport_id)
    competitions = Competition.objects.filter(sport=sport)
    return render(request, "polls/players_competitions.html", {
        "sport": sport,
        "competitions": competitions
    })


# 3️⃣ Teams inside a Competition
@login_required(login_url='/')
def players_teams(request, sport_id, competition_id):
    sport = get_object_or_404(Sport, sport_id=sport_id)
    competition = get_object_or_404(Competition, competition_id=competition_id)
    teams = Team.objects.filter(competition=competition)
    return render(request, "polls/players_teams.html", {
        "sport": sport,
        "competition": competition,
        "teams": teams
    })


# 4️⃣ Players inside a Team
@login_required(login_url='/')
def players_list(request, sport_id, competition_id, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    players = Player.objects.filter(team=team)
    return render(request, "polls/players_list.html", {
        "team": team,
        "players": players
    })


# 5️⃣ Player detail page
#mongo used
@login_required(login_url='/')
def player_detail(request, player_id):
    from .mongo import log_activity

    player = get_object_or_404(Player, player_id=player_id)

    log_activity(
        user=request.user.username,
        action="Viewed Player",
        details={"player_id": player_id, "player_name": player.name}
    )

    return render(request, "polls/player_detail.html", {"player": player})
