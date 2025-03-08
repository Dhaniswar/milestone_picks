from rest_framework.permissions import BasePermission
from .models import Subscription

class HasActiveSubscription(BasePermission):
    def has_permission(self, request, view):
        return Subscription.objects.filter(user=request.user, status='active').exists()