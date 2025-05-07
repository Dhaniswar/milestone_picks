from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import parsers, renderers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import parsers, renderers
from milestone_picks.pagination import CustomPagination
from .models import Sport, Match, Prediction
from .serializers import SportSerializer, MatchSerializer, PredictionSerializer
from subscriptions.permissions import HasActiveSubscription 




class SportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Sport.objects.all().order_by('-id')
    serializer_class = SportSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['id', 'name']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Log to check if the image is being saved properly
        sport = serializer.save()
        if sport.icon:
            print(f"Image file path: {sport.icon.url}")  # Log the file path
            print(f"Image file URL: {sport.icon.url}")    # Log the URL that is generated
        else:
            print("No icon image was provided.")

    def perform_update(self, serializer):
        # Log to check if the image is being saved properly during update
        sport = serializer.save()
        if sport.icon:
            print(f"Image file path: {sport.icon.url}")  # Log the file path
            print(f"Image file URL: {sport.icon.url}") 
    

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('-id')
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'sport', 'team_1', 'team_2', 'match_date', 'location']
    search_fields = ['id', 'sport', 'team_1', 'team_2', 'match_date', 'location']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all().order_by('-id')
    serializer_class = PredictionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user', 'match', 'prediction_type', 'predicted_outcome', 'placed_at', 'result', 'our_prediction', 'confidence_level']
    search_fields = ['id', 'user', 'match', 'prediction_type', 'predicted_outcome', 'placed_at', 'result', 'our_prediction', 'confidence_level']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admins can create, update, or delete bets
            permission_classes = [IsAdminUser]
        else:
            # Authenticated users can view bets (with restrictions)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Prediction.objects.none()
        
        user = self.request.user
        
        if user is None or user.is_anonymous:
            # Return an empty queryset for unauthenticated users
            return Prediction.objects.none()
        
        if user.is_staff:
            # Admins can see all bets
            return Prediction.objects.all()
        
        # Filter bets based on subscription status
        if HasActiveSubscription().has_permission(self.request, self):
            # Users with an active subscription can see all their bets
            return Prediction.objects.filter(user=user)
        else:
            # Users without an active subscription can only see historical bets
            yesterday = timezone.now() - timezone.timedelta(days=1)
            return Prediction.objects.filter(user=user, placed_at__lt=yesterday)

