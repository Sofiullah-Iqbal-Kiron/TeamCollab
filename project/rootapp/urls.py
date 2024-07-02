from django.urls import path

from .views import Index
from .api.endpoints import endpoints
from .api.demo_endpoints import demo_endpoints

app_name = "rootapp"
urlpatterns = [path("", Index.as_view(), name="index")] + endpoints + demo_endpoints
