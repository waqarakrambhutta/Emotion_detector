from django.urls import path
from .views import webcam_view, webcam_feed

urlpatterns = [
    path('', webcam_view, name='webcam_view'),
    path('webcam_feed', webcam_feed, name='webcam_feed'),
]
