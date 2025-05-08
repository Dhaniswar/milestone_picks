from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db import IntegrityError
from milestone_picks import settings
from .models import Sport, Match, Prediction

class SportSerializer(ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name", "icon"]
        extra_kwargs = {'name': {'validators': []}}

    def get_icon(self, obj):
        if obj.icon:
            return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{obj.icon.name}"
        return None

class MatchSerializer(ModelSerializer):
    sport = SportSerializer(read_only=True)
    sport_id = serializers.PrimaryKeyRelatedField(
        queryset=Sport.objects.all(), 
        source='sport',
        write_only=True
    )

    class Meta:
        model = Match
        fields = ["id", "team_1", "team_2", "match_date", "location", "sport", "sport_id"]
        
    def create(self, validated_data):
        sport = validated_data.pop('sport')
        match = Match.objects.filter(
            sport=sport,
            team_1=validated_data['team_1'],
            team_2=validated_data['team_2'],
            match_date=validated_data['match_date']
        ).first()
        
        if not match:
            match = Match.objects.create(sport=sport, **validated_data)
        return match

class PredictionSerializer(ModelSerializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
    match_detail = MatchSerializer(source='match', read_only=True)
    
    class Meta:
        model = Prediction
        fields = [
            "id", "user", "match", "match_detail",
            "prediction_type", "predicted_outcome",
            "our_prediction", "confidence_level",
            "result", "placed_at"
        ]
        extra_kwargs = {
            'user': {
                'read_only': True  # Prevents manual user assignment
            }
        }
    
    def create(self, validated_data):
        try:
            validated_data['user'] = self.context['request'].user
            return Prediction.objects.create(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(str(e))