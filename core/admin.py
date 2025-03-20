from django.contrib import admin
from .models import (HeroSection,
                     SportCategory,
                     ContactUs,
                     FAQ,
                     FAQCategory,
                     Testimonial)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle', 'image']
    
@admin.register(SportCategory)
class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'name', 'icon']
    
@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'message', 'country']


@admin.register(FAQCategory)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    search_fields = ['id', 'name']
    


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'main_heading', 'title', 'title_description', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'title_description']
    



@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'role', 'description', 'image', 'star_rating']
    list_filter = ['id', 'name', 'role', 'description', 'image', 'star_rating']
    search_fields = ['id', 'name', 'role', 'description', 'image', 'star_rating']
    
