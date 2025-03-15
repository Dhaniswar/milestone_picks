from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from .models import Subscription

class HasActiveSubscription(BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return Subscription.objects.filter(user=request.user, status='active').exists()