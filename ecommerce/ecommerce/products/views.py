from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        product_details = cache.get(f'product_{instance.pk}')
        if not product_details:
            serializer = self.get_serializer(instance)
            product_details = serializer.data
            cache.set(f'product_{instance.pk}', product_details, 60 * 60)  # Cache for 1 hour
        return Response(product_details)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.get_queryset(), pk=pk)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        cache.delete(f'product_{instance.pk}')  # Remove cached product details
        return Response({'success': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)