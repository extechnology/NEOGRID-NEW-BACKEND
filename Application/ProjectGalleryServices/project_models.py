from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    location = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank =True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank =True)

    def __str__(self):
        return self.title
    
class ProjectImages(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project/images/') 

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank =True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank =True)

    def __str__(self):
        return self.image.url 


class Gallery(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()

    image= models.ImageField(upload_to = 'gallery/images/')

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank =True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank =True)

    def __str__(self):
        return self.title