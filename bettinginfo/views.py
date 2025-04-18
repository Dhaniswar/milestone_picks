from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers, renderers
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import BettingInfoSection, BettingTip, BettingBasicConcept
from .serializers import (
    BettingInfoSectionSerializer,
    BettingTipSerializer,
    BettingBasicConceptSerializer,
)
from milestone_picks.pagination import CustomPagination





class BettingInfoSectionViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = BettingInfoSection.objects.all().order_by("order")
    serializer_class = BettingInfoSectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "title", "section_type", "is_active"]
    search_fields = ["title", "subtitle", "content"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]







class BettingTipViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = BettingTip.objects.all().order_by("order")
    serializer_class = BettingTipSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "title", "is_active"]
    search_fields = ["title", "content"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]







class BettingBasicConceptViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = BettingBasicConcept.objects.all().order_by("order")
    serializer_class = BettingBasicConceptSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "concept_type", "is_active"]
    search_fields = ["title", "description", "example"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]
