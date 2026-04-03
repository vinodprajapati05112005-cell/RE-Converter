from django.urls import path
from . import views

urlpatterns = [
    path('patterns/', views.list_patterns),
    path('patterns/<str:key>/', views.pattern_detail),
    path('validate/', views.validate),
    path('nlp/', views.nlp_match),
]
