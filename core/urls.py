import os
from django.urls import path, include
from django.http import HttpResponse

# frontend/index.html is at repo root level
_FRONTEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend', 'index.html')

def serve_frontend(request):
    try:
        with open(_FRONTEND, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('<h2>Frontend not found.</h2>', status=404)

urlpatterns = [
    path('', serve_frontend),
    path('api/', include('regex_engine.urls')),
]
