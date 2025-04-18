from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BettingInfoSectionViewSet,
    BettingTipViewSet,
    BettingBasicConceptViewSet,
)

router = DefaultRouter()
router.register(r"betting-info-sections", BettingInfoSectionViewSet)
router.register(r"betting-tips", BettingTipViewSet)
router.register(r"betting-basic-concepts", BettingBasicConceptViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
