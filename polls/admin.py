from django.contrib import admin

from .models import Sport, Competition, Team, Player, Match

admin.site.register(Sport)
admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)

