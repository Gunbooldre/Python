from django.urls import path

from .views import *
urlpatterns = [
    path('api/v1/lead', CreateLeadViewSet.as_view()),
    path('api/v1/app-status/<int:leadId>', GetStatusViewSet.as_view()),
]