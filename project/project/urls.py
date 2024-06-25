from django.contrib import admin
from django.urls import re_path, path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="TeamCollab API",
        default_version='v1',
        description="Interactive documentation for TeamCollab api's",
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny, )
)

urlpatterns = [
    # admin app
    path('admin/', admin.site.urls),

    # third party apps
    path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('knox.urls')),
    path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),

    # local apps
    path('api/', include('rootapp.urls')),
]
