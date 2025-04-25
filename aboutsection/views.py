from rest_framework.viewsets import ModelViewSet
from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    AboutSection,
    Statistic,
    MissionSection,
    WhyChooseUs,
    Feature,
    BettingPhilosophy,
    ValueProposition,
    ValueItem,
    Testimonial,
    CallToAction,
)
from .serializers import (
    AboutSectionSerializer,
    StatisticSerializer,
    MissionSectionSerializer,
    WhyChooseUsSerializer,
    FeatureSerializer,
    BettingPhilosophySerializer,
    ValuePropositionSerializer,
    ValueItemSerializer,
    TestimonialSerializer,
    CallToActionSerializer,
    AboutPageSerializer,
)
from milestone_picks.pagination import CustomPagination





class AboutSectionViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = AboutSection.objects.all()
    serializer_class = AboutSectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["main_title", "main_description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]




class StatisticViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Statistic.objects.all().order_by("order")
    serializer_class = StatisticSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "section", "is_active"]
    search_fields = ["number", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]




class MissionSectionViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = MissionSection.objects.all().order_by("order")
    serializer_class = MissionSectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]





class WhyChooseUsViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = WhyChooseUs.objects.all().order_by("order")
    serializer_class = WhyChooseUsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]




class FeatureViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Feature.objects.all().order_by("order")
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]





class BettingPhilosophyViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = BettingPhilosophy.objects.all().order_by("order")
    serializer_class = BettingPhilosophySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]






class ValuePropositionViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = ValueProposition.objects.all().order_by("order")
    serializer_class = ValuePropositionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]






class ValueItemViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = ValueItem.objects.all().order_by("order")
    serializer_class = ValueItemSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "proposition", "is_active"]
    search_fields = ["title", "description"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]






class TestimonialViewSet(ModelViewSet):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    queryset = Testimonial.objects.all().order_by("order")
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["quote", "author", "position"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]





class CallToActionViewSet(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = CallToAction.objects.all().order_by("order")
    serializer_class = CallToActionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["id", "is_active"]
    search_fields = ["title", "description", "button_text"]
    pagination_class = CustomPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]





class AboutPageAPIView(ModelViewSet):
    renderer_classes = (renderers.JSONRenderer,)
    queryset = AboutSection.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        try:
            about_section = AboutSection.objects.first()
            mission_section = MissionSection.objects.first()
            why_choose_us = WhyChooseUs.objects.first()
            betting_philosophy = BettingPhilosophy.objects.first()
            testimonial = Testimonial.objects.first()
            call_to_action = CallToAction.objects.first()

            if not all(
                [
                    about_section,
                    mission_section,
                    why_choose_us,
                    betting_philosophy,
                    testimonial,
                    call_to_action,
                ]
            ):
                return Response(
                    {"error": "About page content not fully configured"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = AboutPageSerializer(
                {
                    "about_section": about_section,
                    "mission_section": mission_section,
                    "why_choose_us": why_choose_us,
                    "betting_philosophy": betting_philosophy,
                    "testimonial": testimonial,
                    "call_to_action": call_to_action,
                }
            )

            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
