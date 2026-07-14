from django.template.defaultfilters import default
from django.db import models


class PhoneNumbers(models.Model):
    phone_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number + " - " + self.name
    
    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
    