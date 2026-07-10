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

class Dealers(models.Model):
    unique_id = models.CharField(max_length=10, unique=True, default=create_dealer_id)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null = True, blank = True)
    dealer_type = models.CharField(max_length = 200, null = True, blank = True)
    dealer_name = models.CharField(max_length = 200)
    dealer_description = models.CharField(max_length = 200 , null = True, blank = True)
    dealer_email = models.CharField(max_length = 200)
    dealer_phone = models.CharField(max_length = 200)
    dealer_website = models.CharField(max_length = 200, null = True, blank = True)
    dealer_address = models.CharField(max_length = 200)
    dealer_city = models.CharField(max_length = 200)
    dealer_state = models.CharField(max_length = 200)
    dealer_pincode = models.CharField(max_length = 200)
    dealer_country = models.CharField(max_length = 200, default = 'India')
    dealer_location_iframe = models.TextField(help_text='Copy and paste the google map iframe code here')
    dealer_status = models.CharField(max_length = 200,choices=DEALER_STATUS,default="PENDING")
    is_main = models.BooleanField(default = False)
    dealer_created_at = models.DateTimeField(auto_now_add=True)
    dealer_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dealer_name

    class Meta:
        verbose_name = '4. Dealer'
        verbose_name_plural = '4. Dealers'

class WarrentyRegisterModel(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    dealer = models.ForeignKey(Dealers,on_delete=models.CASCADE)
    pincode = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    model_number = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    purchased_date = models.DateField()

    def __str__(self):
        return self.fullname

