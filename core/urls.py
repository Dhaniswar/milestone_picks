from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HeroSectionViewSet, SportCategoryViewSet, ContactUsViewSet

router = DefaultRouter()
router.register(r'sport-category', SportCategoryViewSet)
router.register(r'hero-section', HeroSectionViewSet)
router.register(r'contact-us', ContactUsViewSet)
urlpatterns = [
    path('', include(router.urls)),    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)