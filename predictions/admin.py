from django.contrib import admin
from .models import Sport, Match, Prediction

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']
    
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'sport', 'team_1', 'team_2', 'match_date', 'location']
    
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'match', 'prediction_type', 'predicted_outcome', 'placed_at', 'result']