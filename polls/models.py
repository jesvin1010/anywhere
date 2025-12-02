from django.db import models


class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name



class Competition(models.Model):
    competition_id = models.AutoField(primary_key=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='competitions')
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    season = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.season})" if self.name else f"Competition {self.competition_id}"



class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else f"Team {self.team_id}"



class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else f"Player {self.player_id}"



class Match(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Live', 'Live'),
        ('Finished', 'Finished'),
        ('Postponed', 'Postponed'),
    ]

    match_id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.status})"
