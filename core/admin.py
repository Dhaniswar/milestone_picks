from django.contrib import admin
from .models import HeroSection, SportCategory, ContactUs


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle', 'image']
    
@admin.register(SportCategory)
class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'name', 'icon']
    
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'message', 'country']
    
