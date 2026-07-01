from django.db import models

class HomeSlider(models.Model):
    image = models.ImageField(upload_to='uploads/home_slider')
    title = models.CharField(max_length=255)
    title_2 = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


