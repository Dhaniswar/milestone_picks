from rest_framework.serializers import ModelSerializer, SerializerMethodField
from milestone_picks import settings
from .models import Sport, Match, Prediction


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name", "icon"]
        extra_kwargs = {
            'name': {'validators': []}
        }

    def get_icon(self, obj):
        if obj.icon:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{obj.icon.name}"
        return None


class MatchSerializer(ModelSerializer):
    sport = SportSerializer()

    class Meta:
        model = Match
        fields = ["id", "team_1", "team_2", "match_date", "location", "sport"]
        
    def create(self, validated_data):
        sport_data = validated_data.pop('sport')
        sport, _ = Sport.objects.get_or_create(**sport_data)
        return Match.objects.create(sport=sport, **validated_data)



class PredictionSerializer(ModelSerializer):
    match = MatchSerializer()

    class Meta:
        model = Prediction
        fields = [
            "id",
            "user",
            "prediction_type",
            "predicted_outcome",
            "placed_at",
            "result",
            "our_prediction",
            "confidence_level",
            "match",
        ]
    
    def create(self, validated_data):
        match_data = validated_data.pop('match')
        match_serializer = MatchSerializer(data=match_data)
        match_serializer.is_valid(raise_exception=True)
        match = match_serializer.save()
        
        return Prediction.objects.create(match=match, **validated_data)
