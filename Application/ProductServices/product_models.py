from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify

class ProductDepartment(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length = 200)
    image = models.ImageField(upload_to='images/products/department',null=True, blank=True, help_text='Image for the product department, not mandatory')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    slug = models.SlugField(unique=True, null = True, blank = True, help_text='auto generate on save')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Product Department'
        verbose_name_plural = 'Product Departments'

class ProductFamily(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/products/family',null=True, blank=True, help_text='Image for the product department, not mandatory')

    department = models.ForeignKey(ProductDepartment, on_delete=models.CASCADE, related_name='families')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} - {self.department.name}"
    
    class Meta:
        verbose_name = 'Product Family'
        verbose_name_plural = 'Product Families'        

class Product(models.Model):
    family = models.ForeignKey(ProductFamily, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    
    model_type = models.CharField(max_length=100, null=True, blank=True)
    model_number = models.CharField(max_length=100 , null=True, blank=True)
    
    price=models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    description=HTMLField(null=True,blank=True)
    additional_info=HTMLField(null=True,blank=True)
    technical_spec=HTMLField(null=True,blank=True)
    warrenty_info = HTMLField(null=True,blank=True)
    new_arrival=models.BooleanField(default=False)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'        

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/products',null=True, blank=True, help_text='Image for the product, not mandatory')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'