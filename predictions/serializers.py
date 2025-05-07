from rest_framework.serializers import ModelSerializer, SerializerMethodField
from milestone_picks import settings
from .models import Sport, Match, Prediction


class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name", "icon"]

    def get_icon(self, obj):
        if obj.icon:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{obj.icon.name}"
        return None


class MatchSerializer(ModelSerializer):
    sport = SportSerializer()

    class Meta:
        model = Match
        fields = ["id", "team_1", "team_2", "match_date", "location", "sport"]


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
