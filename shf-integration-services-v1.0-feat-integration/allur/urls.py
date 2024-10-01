from django.urls import path
from rest_framework import routers

from .views import LeadViewSet

app_name = "allur"

router = routers.DefaultRouter()

router.register("allur", LeadViewSet, basename="allur")

urlpatterns = router.urls