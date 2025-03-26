from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from milestone_picks import settings
import os

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import  TokenRefreshView
from subscriptions.views import success_view
from .greet import Greet
from user.views import CustomTokenObtainPairView, CustomTokenRefreshView

# Swagger schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Milestone Picks",
      default_version='v1',
      description="Milestone description",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
    # url="https://1afb-103-156-26-47.ngrok-free.app",

)

urlpatterns = [
    path('', Greet.as_view(), name='greet'),
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('core/', include('core.urls')),
    path('user/', include('user.urls')),
    path('predictions/', include('predictions.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('success/', success_view, name='success'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

if os.environ.get('DEBUG'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)