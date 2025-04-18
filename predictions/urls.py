from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportViewSet, MatchViewSet, PredictionViewSet

router = DefaultRouter()
router.register(r'sports', SportViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'', PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
