from django.contrib import admin
from .models import Category,Status,Value,CommonValue,Phone,Watch,Image,Chart,Shipping,Billing

admin.site.register([Status,Category,Value,CommonValue,Phone,Watch,Image,Chart,Shipping,Billing])
# Register your models here.
