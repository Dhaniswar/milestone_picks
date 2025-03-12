from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)



schema_view = get_schema_view(
   openapi.Info(
      title="Milestone Picks",
      default_version='v1',
      description="Milestone description",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   # url="https://680d-103-156-26-46.ngrok-free.app",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('core/', include('core.urls')),
    path('user/', include('user.urls')),
    path('predictions/', include('predictions.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
