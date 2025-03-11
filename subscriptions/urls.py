# urls.py
from django.urls import path, include
from .views import CreateCheckoutSessionView, stripe_webhook
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet),
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('', include(router.urls)),
]