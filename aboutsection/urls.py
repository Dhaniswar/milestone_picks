from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AboutSectionViewSet,
    StatisticViewSet,
    MissionSectionViewSet,
    WhyChooseUsViewSet,
    FeatureViewSet,
    BettingPhilosophyViewSet,
    ValuePropositionViewSet,
    ValueItemViewSet,
    TestimonialViewSet,
    CallToActionViewSet,
    AboutPageAPIView,
)

router = DefaultRouter()
router.register(r"about-sections", AboutSectionViewSet, basename="aboutsection")
router.register(r"statistics", StatisticViewSet, basename="statistic")
router.register(r"mission-sections", MissionSectionViewSet, basename="missionsection")
router.register(r"why-choose-us", WhyChooseUsViewSet, basename="whychooseus")
router.register(r"features", FeatureViewSet, basename="feature")
router.register(
    r"betting-philosophies", BettingPhilosophyViewSet, basename="bettingphilosophy"
)
router.register(
    r"value-propositions", ValuePropositionViewSet, basename="valueproposition"
)
router.register(r"value-items", ValueItemViewSet, basename="valueitem")
router.register(r"testimonials", TestimonialViewSet, basename="testimonial")
router.register(r"call-to-actions", CallToActionViewSet, basename="calltoaction")

urlpatterns = [
    path("", include(router.urls)),
    path("about-page/", AboutPageAPIView.as_view({"get": "list"}), name="about-page"),
]
