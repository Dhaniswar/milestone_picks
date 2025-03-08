from django.contrib import admin
from .models import Plan, Subscription

@admin.register(Plan)
class SportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stripe_plan_id', 'price', 'duration']
   
    
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'plan', 'stripe_subscription_id', 'status', 'start_date', 'end_date']

    