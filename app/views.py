import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CartItem
from .serializers import CartItemSerializer
from decimal import Decimal

PRICE_API_BASE_URL = "http://localhost:3001/products/"

class ShoppingCartView(APIView):

    def get_price(self, product_name):
        response = requests.get(f"{PRICE_API_BASE_URL}{product_name}")
        if response.status_code == 200:
            return response.json().get("price", 0)
        return None

    def get(self, request):
        cart_items = CartItem.objects.all()
        subtotal = sum(item.total_price() for item in cart_items)
        tax = round(subtotal * Decimal('0.125'), 2)
        total = round(subtotal + tax, 2)
        
        return Response({
            "cart": CartItemSerializer(cart_items, many=True).data,
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        })

    def post(self, request):
        product_name = request.data.get("product_name")
        quantity = request.data.get("quantity", 1)

        price = self.get_price(product_name)
        if price is None:
            return Response({"error": "Invalid product name"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(product_name=product_name, defaults={"quantity": 0, "price": price})
        cart_item.quantity += int(quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
