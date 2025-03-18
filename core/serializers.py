from rest_framework import serializers
from .models import HeroSection, SportCategory, ContactUs

class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['id', 'title', 'subtitle', 'image']



class SportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = ['id', 'title', 'name', 'icon']


class ContactUsSerialiser(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUs
        fields = ['id', 'full_name', 'email', 'phone', 'message', 'country']