import random

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, User
from .serializers import ProductSerializer
from .producer import publish

class ProductViewSet(viewsets.ViewSet):
    # /api/product
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # /api/product
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # /api/product/<str:id>
    def retrieve(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # /api/product/<str:id>
    def update(self, request, pk=None):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    # /api/product/<str:id>
    def distroy(self, request, pk=None):
        product = Product.objects.get(id=pk)
        if product is not None:
            product.delete()
            publish('product_deleted',pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id' : user.id
        })

# Create your views here.
