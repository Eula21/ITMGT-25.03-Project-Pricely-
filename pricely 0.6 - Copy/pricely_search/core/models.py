from django.db import models
from django.contrib.auth.models import User # LYSS: Added this for my list feature!


# CORINNE JUL 10: added a Product model to act as a database for the scraped data 
class Product(models.Model):
    product_title = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)  
    shop_name = models.CharField(max_length=200, blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    product_url = models.URLField()
    image_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.product_title
    
# LYSS: These two classes are for my list feature. LISTITEM connected to a LIST connected to a USER (ListItem -> List -> User)

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    




