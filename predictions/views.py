from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import parsers, renderers
from milestone_picks.pagination import CustomPagination
from .models import Sport, Match, Bet
from .serializers import SportSerializer, MatchSerializer, BetSerializer
from subscriptions.permissions import HasActiveSubscription 




class SportViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Sport.objects.all()
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
        # if sport.icon:
        #     print(f"Image file path: {sport.icon.url}")  # Log the file path
        #     print(f"Image file URL: {sport.icon.url}") 
    

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
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
    
    


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id', 'user', 'match', 'bet_type', 'odds', 'amount', 'placed_at', 'result']
    search_fields = ['id', 'user', 'match', 'bet_type', 'odds', 'amount', 'placed_at', 'result']
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
        user = self.request.user
        if user.is_staff:
            # Admins can see all bets
            return Bet.objects.all()
        
        # Filter bets based on subscription status
        if HasActiveSubscription().has_permission(self.request, self):
            # Users with an active subscription can see all their bets
            return Bet.objects.filter(user=user)
        else:
            # Users without an active subscription can only see historical bets
            yesterday = timezone.now() - timezone.timedelta(days=1)
            return Bet.objects.filter(user=user, placed_at__lt=yesterday)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the bet creator
        serializer.save(user=self.request.user)