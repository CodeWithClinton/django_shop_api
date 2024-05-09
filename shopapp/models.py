from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="img")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name 
    
class Cart(models.Model):
    session_key = models.CharField(max_length=50)

    def __str__(self):
        return self.session_key



class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitems")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"cartitem - {self.product.name}"