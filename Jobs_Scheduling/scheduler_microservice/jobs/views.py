from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import logging
from .models import Job
from .serializers import JobSerializer

logger = logging.getLogger(__name__)

class JobPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class JobRateThrottle(UserRateThrottle):
    rate = '100/minute'

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = JobPagination
    throttle_classes = [JobRateThrottle]

    @action(detail=True, methods=['post'])
    def mark_as_run(self, request, pk=None):
        job = self.get_object()
        job.mark_as_run()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

    @method_decorator(cache_page(60*15))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                {"error": "Failed to create job", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @method_decorator(cache_page(60*5))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)