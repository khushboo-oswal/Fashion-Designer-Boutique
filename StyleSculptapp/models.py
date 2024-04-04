from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CATEGORY=(1,'Blouse'),(2,'One-Piece'),(3,'Jumpsuit'),(4,'Co-ord Sets')
    name=models.CharField(max_length=100)
    detail=models.CharField(max_length=300)
    category=models.IntegerField(verbose_name='Categories',choices=CATEGORY)
    fabric=models.CharField(max_length=300)
    size=models.IntegerField()
    color=models.CharField(max_length=100)
    price=models.FloatField()
    is_active=models.BooleanField(default=True)
    image=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class Cart(models.Model):
    #auth.user means auth file me jo user table hai usko call kiya hai
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    # ondelete cascade is written as on_delete=models.CASCADE
    # db_column is used for aliasings
    #product direct likha hai kyuki yeh product table ka class humne yehi file me create kiya hai
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField(default=1)

class Order(models.Model):
    #fetch product detail from cart table for authenticated user
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField(default=1)
    amt=models.FloatField()

    #after payment order table ka order history me and then order table mese delete karna hai

class History(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField(default=1)
    amt=models.FloatField()

class Address(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    address=models.CharField(max_length=300)