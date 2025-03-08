from rest_framework import serializers
from .models import Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'stripe_plan_id', 'price', 'duration']



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'stripe_subscription_id', 'status', 'start_date', 'end_date']


class CreateCheckoutSessionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()