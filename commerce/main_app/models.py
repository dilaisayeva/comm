from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.utils.text import slugify
import re
import string 
from django.utils.text import slugify 
import datetime
import random

# Create your models here.

class Status(models.Model):
    status = models.CharField(max_length=120)
    
    def __str__(self):
        return self.status + ' ' + str(self.id)


class Category(models.Model):
    name = models.CharField(max_length=120)
    status = models.ForeignKey('Status',on_delete=models.CASCADE,blank=True,null=True)
    cat = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.name  + ' ' + str(self.id)

# class Color(models.Model):
#     name = models.CharField(max_length=120)
#     status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='status_color')
    
#     def __str__(self):
#         return self.name

class Phone(models.Model):
    name = models.CharField(max_length=120)
    color = ColorField(default='#FF0000')
    status = models.ForeignKey('Status',on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='phone',blank=True,null=True)
    description = models.CharField(max_length=500)
    cat = models.ForeignKey('Category',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dual = models.ForeignKey('CommonValue',on_delete=models.CASCADE,blank=True,null=True,related_name='dual')
    memory = models.CharField(max_length=50)
    os =models.ForeignKey('CommonValue',on_delete=models.CASCADE,blank=True,null=True,related_name='os')
    connectivity = models.CharField(max_length=50,blank=True,null=True)
    camera = models.CharField(max_length=50)
    battery = models.CharField(max_length=50)
    hearing = models.CharField(("Hearing Aid Compatibility"), max_length=50,blank=True,null=True)
    dimensions =models.CharField(max_length=50,blank=True,null=True,default="Salam")
    display =models.CharField(max_length=50,blank=True,null=True)
    brand =models.ForeignKey('CommonValue',on_delete=models.CASCADE,blank=True,null=True)
    price= models.DecimalField(max_digits=8, decimal_places=2)
    currency=models.CharField(max_length=50)
    quantity=models.IntegerField(default=1)
    like = models.ManyToManyField(User,related_name='like',blank=True)
    slug = models.SlugField(unique=True)

 
    def save(self, *args, **kwargs):
        string.digits
        self.slug =slugify(string.digits.join(random.sample(string.ascii_lowercase, 4)))
        super(Phone, self).save(*args, **kwargs)
       
    def __str__(self):
        return self.name + ' ' + str(self.id)
    

class Watch(models.Model):
    name = models.CharField(max_length=120)
    color = ColorField(default='#FF0000')
    status = models.ForeignKey('Status',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None)
    description = models.CharField(max_length=500)
    cat = models.ForeignKey('Category',on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memory = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    Health = models.CharField(("Health & Fitness Features"),max_length=50,blank=True,null=True)
    water_resistance = models.CharField(max_length=50)
    communication = models.CharField(max_length=50)
    wireless = models.CharField( max_length=50,blank=True,null=True)


class Value(models.Model):
    name = models.CharField(max_length=120)
    status = models.ForeignKey('Status',on_delete=models.CASCADE)
    def __str__(self):
        return self.name + ' ' + str(self.id)

class CommonValue(models.Model):
    name = models.CharField(max_length=120)
    status = models.ForeignKey('Status',on_delete=models.CASCADE)
    val = models.ForeignKey('Value',on_delete=models.CASCADE)
    cat = models.ForeignKey('Category',on_delete=models.CASCADE,blank=True,null=True)
    # product = models.ForeignKey("Product",on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name + ' ' + str(self.id)

def get_cat():
    return Category.objects.get(id=4)

class Image(models.Model):
    image = models.ImageField(upload_to="phone",blank=True,null=True)
    product = models.ForeignKey('Phone',on_delete=models.CASCADE,blank=True,null=True)
    cat = models.ForeignKey("Category",on_delete=models.CASCADE,blank=True,null=True,default='4')
    def __str__(self):
        return self.product.name 


class Chart(models.Model):
    product = models.ForeignKey("Phone", on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True,null=True)
    total = models.DecimalField(max_digits=8, decimal_places=4,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.product.name + ' ' + str(self.id) + ' ' + str(self.product.id)

Shipping_choies = [
    ('10.00', 'Flat rate: $10.00'),
    ('5.00', 'Flat rate: $5.00'),
    ('2.00', 'Local delivery : $2.00'),
    ('0', 'Free shipping'),
   
]

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50,blank=True,null=True)
    shipping = models.CharField(max_length=50 )
    
    def __str__(self):
        return self.shipping

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname= models.CharField( max_length=50)
    lastname=models.CharField( max_length=50)
    company=models.CharField( max_length=50)
    phone=models.CharField( max_length=50)
    email=models.CharField( max_length=50)
    country=models.CharField( max_length=50)
    address_01=models.CharField( max_length=50)
    address_02=models.CharField( max_length=50)
    town_city=models.CharField( max_length=50)
    district=models.CharField( max_length=50)
    postcode=models.CharField(max_length=50)
     
    