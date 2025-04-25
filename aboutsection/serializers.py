from rest_framework import serializers
from .models import (
    AboutSection,
    Statistic,
    MissionSection,
    WhyChooseUs,
    Feature,
    BettingPhilosophy,
    ValueProposition,
    ValueItem,
    Testimonial,
    CallToAction,
)





class AboutSectionSerializer(serializers.ModelSerializer):
    top_statistics = serializers.SerializerMethodField()
    bottom_statistics = serializers.SerializerMethodField()

    class Meta:
        model = AboutSection
        fields = "__all__"

    def get_top_statistics(self, obj):
        stats = Statistic.objects.filter(section="top")
        return StatisticSerializer(stats, many=True).data

    def get_bottom_statistics(self, obj):
        stats = Statistic.objects.filter(section="bottom")
        return StatisticSerializer(stats, many=True).data


class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = '__all__'
        ref_name = 'about_about_section'  # Unique ref name

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = '__all__'
        ref_name = 'about_statistic'

class MissionSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionSection
        fields = '__all__'
        ref_name = 'about_mission_section'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'
        ref_name = 'about_feature'

class WhyChooseUsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = WhyChooseUs
        fields = '__all__'
        ref_name = 'about_why_choose_us'

class ValueItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueItem
        fields = '__all__'
        ref_name = 'about_value_item'

class ValuePropositionSerializer(serializers.ModelSerializer):
    items = ValueItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = ValueProposition
        fields = '__all__'
        ref_name = 'about_value_proposition'

class BettingPhilosophySerializer(serializers.ModelSerializer):
    value_proposition = ValuePropositionSerializer(read_only=True)
    
    class Meta:
        model = BettingPhilosophy
        fields = '__all__'
        ref_name = 'about_betting_philosophy'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        ref_name = 'about_testimonial'  # Unique ref name different from core

class CallToActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallToAction
        fields = '__all__'
        ref_name = 'about_call_to_action'

class AboutPageSerializer(serializers.Serializer):
    about_section = AboutSectionSerializer()
    mission_section = MissionSectionSerializer()
    why_choose_us = WhyChooseUsSerializer()
    betting_philosophy = BettingPhilosophySerializer()
    testimonial = TestimonialSerializer()
    call_to_action = CallToActionSerializer()
    
    class Meta:
        ref_name = 'about_page'  # Unique ref name for the combined serializer