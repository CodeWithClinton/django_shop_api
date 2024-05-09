from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Cart, CartItem, Product 
from .serializers import CartItemSerializer, ProductSerializer
# Create your views here.

@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



class CartItemModelViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    @action(detail=False, methods=["GET"])
    def cartitem_quantity(self, request):
        product_id = request.query_params.get("product_id")
        cart_id = request.query_params.get("cart_id")

        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            quantity = cartitem.quantity
            return Response(quantity)
        except:
            quantity = 0
            return Response(quantity)

    @action(detail=True, methods=['PATCH'])
    def update_item(self, request, pk):
        try:
            cartitem = self.get_object()
            quantity = int(request.data.get("quantity", 0))
            if quantity >= 1:
                cartitem.quantity = quantity
                cartitem.save()
                serializer = CartItemSerializer(cartitem)
                return Response({"data": serializer.data, "message": "Cartitem updated successfully"})
            else:
                cartitem.delete()
                return Response({'message': 'Item deleted because quantity is less than 1'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        try:
            product_id = request.data.get("product_id")

            session_key = request.session.session_key
            
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
            cartitem, created = CartItem.objects.get_or_create(product_id=product_id, cart=cart)

            if not created:
                cartitem.quantity += 1
                cartitem.save() 
            
            else:
                cartitem.quantity = 1 
                cartitem.save
            serializer = CartItemSerializer(cartitem)
            return Response({"data": serializer.data, "message": "Cartitem created successfully"})
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            