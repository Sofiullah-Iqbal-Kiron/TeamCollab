from django.urls import path

from .views import Index
from .api.endpoints import endpoints

app_name = "rootapp"
urlpatterns = [path("", Index.as_view(), name="index")] + endpoints
