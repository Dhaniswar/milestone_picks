from django.contrib import admin
from .models import HeroSection, SportCategory


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle', 'image']
    
@admin.register(SportCategory)
class SportCategory(admin.ModelAdmin):
    list_display = ['id', 'title', 'name', 'icon']
    
