from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(upload_to='category_image')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(upload_to='product_image')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    availability = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)  #one time
    updated = models.DateTimeField(auto_now=True)   #change everytime we update a record

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
