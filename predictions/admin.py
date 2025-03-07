from django.contrib import admin
from .models import Sport, Match, Bet

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'sport', 'team_1', 'team_2', 'match_date', 'location']
    
@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'match', 'bet_type', 'odds', 'amount', 'placed_at', 'result']