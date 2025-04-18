from django.contrib import admin
from .models import BettingInfoSection, BettingTip, BettingBasicConcept


@admin.register(BettingInfoSection)
class BettingInfoSectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "section_type", "order", "is_active"]
    list_filter = ["section_type", "is_active"]
    search_fields = ["title", "subtitle", "content"]
    list_editable = ["order", "is_active"]
    ordering = ["order"]


@admin.register(BettingTip)
class BettingTipAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "content"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]


@admin.register(BettingBasicConcept)
class BettingBasicConceptAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "concept_type", "order", "is_active"]
    list_filter = ["concept_type", "is_active"]
    search_fields = ["title", "description", "example"]
    list_editable = ["order", "is_active"]
    ordering = ["order"]
