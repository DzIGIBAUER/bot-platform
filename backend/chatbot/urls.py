from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ChatbotViewset

router = DefaultRouter()
router.register(r'', ChatbotViewset, basename='chatbot')


urlpatterns = router.urls
