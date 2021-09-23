from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Category(models.Model): 
    title = models.CharField(max_length=50)
    img= models.ImageField(upload_to='category/', default= 'img.jpg')

    def __str__(self):
        return self.title  

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 


class Product(models.Model):
    category =models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    price = models.FloatField() 
    min_quantity = models.IntegerField(default=1)
    max_quantity = models.IntegerField(default=20)
    img = models.ImageField(upload_to='shop/', default= 'img.jpg')
    description = models.TextField()
    available = models.BooleanField()
    featured = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False) 

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'product'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'



class ProfileDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    phone = models.CharField(max_length= 50)
    address = models.CharField(max_length= 50)
    city = models.CharField(max_length= 50)
    state = models.CharField(max_length= 50)
    image = models.ImageField(upload_to='userdetail/', default='profile.jpg', blank=True, null=True)


    def __str__(self):
        return self.user.username

    
    class Meta:
        db_table = 'profiledetail'
        managed = True
        verbose_name = 'ProfileDetail'
        verbose_name_plural = 'ProfileDetails'


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart_code = models.CharField(max_length=50)
    paid_order = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username



class PaidOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_paid = models.IntegerField()
    cart_code = models.CharField(max_length=36)
    transac_code = models.CharField(max_length=12)
    paid_order = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    phone = models.CharField(max_length= 50)
    address = models.CharField(max_length= 50)
    city = models.CharField(max_length= 50)
    state = models.CharField(max_length= 50)

    def __str__(self):
        return self.user.username

