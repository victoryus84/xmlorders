from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    is_active = models.BooleanField(default=False)
    level = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        # constraints = [
        #     models.CheckConstraint(check=~Q(name=''), name='name_not_empty'),
        # ]

    # def clean(self):
    #     super().clean()
    #     if self.name == '':
    #         raise ValidationError({'name': "This field cannot be empty."})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.DecimalField(max_digits=15, decimal_places=3)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('delivered', 'Delivered'),
    ]
    representative = models.ForeignKey(User, on_delete=models.CASCADE)
    client =  models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.status} - {self.client} "

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"{self.order.id} - {self.product.name} - {self.quantity}"    
