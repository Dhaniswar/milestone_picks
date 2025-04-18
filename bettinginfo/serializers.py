from rest_framework import serializers
from .models import BettingInfoSection, BettingTip, BettingBasicConcept


class BettingInfoSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BettingInfoSection
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "image",
            "section_type",
            "order",
            "is_active",
        ]


class BettingTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = BettingTip
        fields = ["id", "title", "slug", "content", "image", "order", "is_active"]


class BettingBasicConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = BettingBasicConcept
        fields = [
            "id",
            "title",
            "concept_type",
            "description",
            "example",
            "icon",
            "order",
            "is_active",
        ]
