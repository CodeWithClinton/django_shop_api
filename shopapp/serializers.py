from rest_framework import serializers 
from .models import Product, Cart, CartItem 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ['id', "name", "image", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem 
        fields = ["id", "product", "product_id",  "quantity", "sub_total"]

    
    def get_sub_total(self, cartitem):
        total_price = cartitem.quantity * cartitem.product.price 
        return total_price


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_cartitems = serializers.SerializerMethodField()
    cartitems = CartItemSerializer(read_only=True, many=True)
    class Meta:
        model = Cart 
        fields = ["id", "session_key", "cartitems", "total_cartitems", "total_price"]

    def get_total_price(self, cart):
        total_price = sum([item.quantity  * item.product.price for item in cart.cartitems.all()])
        return total_price
    
    def get_total_cartitems(self, cart):
        total_cartitems = sum([item.quantity for item in cart.cartitems.all()])
        return total_cartitems