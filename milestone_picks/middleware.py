# middleware.py
from django.http import JsonResponse

class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return JsonResponse({"status": "ok", "message": "Application is healthy"})
        return self.get_response(request)