from random import choices
from Application.ProductServices import product_serializers
from django.db import models


def create_dealer_id():
    import random
    import string
    return 'DEAL' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def create_warrenty_id():
    import random
    import string
    return 'WAR' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

DEALER_STATUS = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
    ('PENDING', 'Pending'),
)

class Country(models.Model):
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '1. Country'
        verbose_name_plural = '1. Countries'

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '2. State'
        verbose_name_plural = '2. States'

class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '3. District'
        verbose_name_plural = '3. Districts'



class MainFranchaseModel(models.Model):
    name = models.CharField(max_length=100)

    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    pincode = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)

    location_link = models.CharField(max_length=300)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubFranchaseModel(models.Model):
    main_franchase = models.ForeignKey(MainFranchaseModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100)

    location_link = models.CharField(max_length=300)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class WarrantyRegisterModel(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    franchise = models.CharField(max_length=200)
    product_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    purchased_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.fullname

