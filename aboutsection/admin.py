from django.contrib import admin
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


class StatisticAdmin(admin.ModelAdmin):
    list_display = ("number", "description", "section", "order")
    list_filter = ("section",)
    ordering = ("section", "order")


class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    ordering = ("order",)


class ValueItemInline(admin.TabularInline):
    model = ValueItem
    extra = 1


class ValuePropositionAdmin(admin.ModelAdmin):
    inlines = [ValueItemInline]


admin.site.register(AboutSection)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(MissionSection)
admin.site.register(WhyChooseUs)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(BettingPhilosophy)
admin.site.register(ValueProposition, ValuePropositionAdmin)
admin.site.register(Testimonial)
admin.site.register(CallToAction)
