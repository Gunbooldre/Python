from django.urls import path
from rest_framework import routers

from .views import BitrixViewSet

app_name = "bitrix24"

router = routers.DefaultRouter()

router.register("bitrix/", BitrixViewSet, basename="bitrix")

urlpatterns = router.urls