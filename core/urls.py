from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroSectionViewSet, SportCategoryViewSet, ContactUsViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'sport-category', SportCategoryViewSet)
router.register(r'hero-section', HeroSectionViewSet)
router.register(r'contact-us', ContactUsViewSet)
router.register(r'faqs', FAQViewSet)
urlpatterns = [
    path('', include(router.urls)),    
]
