from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Sport, Match, Bet

class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'name', 'icon']
    

class MatchSerializer(ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'sport', 'team_1', 'team_2', 'match_date', 'location']


class BetSerializer(ModelSerializer):
    payout = SerializerMethodField()
    class Meta:
        model = Bet
        fields = ['id', 'user', 'match', 'bet_type', 'odds', 'amount', 'placed_at', 'result', 'payout']
    
    def get_payout(self, obj):
        return obj.calculate_payout()
    