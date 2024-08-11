from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'jobs', JobViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Scheduler Microservice API",
      default_version='v1',
      description="API for managing scheduled jobs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]