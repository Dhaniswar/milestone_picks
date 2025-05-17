from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse

class Greet(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # For normal requests
        return Response({
            "message": "Hello, Welcome to Milestone Picks",
            "status": "healthy"
        }, status=status.HTTP_200_OK)

# Add this simple view function in the same file
def health_check(request):
    """Simplest possible health check for load balancer"""
    return HttpResponse("OK", status=200)
