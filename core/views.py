from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from milestone_picks.pagination import CustomPagination
from .models import HeroSection, SportCategory, ContactUs, FAQ
from .serializers import HeroSectionSerializer, SportCategorySerializer, ContactUsSerialiser, FAQSerializer


class HeroSectionViewSet(ModelViewSet):
    queryset = HeroSection.objects.all().order_by('-id')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = HeroSectionSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['id', 'title', 'subtitle']
    search_fields = ['id', 'title', 'subtitle']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    




class SportCategoryViewSet(ModelViewSet):
    queryset = SportCategory.objects.all().order_by('-id')
    serializer_class = SportCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['id', 'name']
    search_fields = ['id', 'title', 'name'] 
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    

class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-id')
    serializer_class = ContactUsSerialiser
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    filterset_fields = ['id', 'full_name', 'email', 'phone', 'message']
    search_fields = ['id', 'full_name', 'email', 'phone', 'message']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    
    
class FAQViewSet(ModelViewSet):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [AllowAny]
    search_fields = ['title', 'title_description']
    filterset_fields = ['order']
    pagination_class = CustomPagination
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

