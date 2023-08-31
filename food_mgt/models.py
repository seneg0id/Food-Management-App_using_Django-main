from distutils.command.upload import upload
from email.policy import default
from pickle import TRUE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from datetime import date

#create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=100)
    date = models.DateField()
    date_posted = models.DateTimeField(default = timezone.now)
    #status = models.CharField(max_length=100)
    image = models.ImageField(upload_to='food_pics')
    state = models.CharField(max_length=100,null=TRUE)
    city  = models.CharField(max_length=100,null=TRUE)
    status = models.CharField(max_length=100,default='Available')
    booked = models.CharField(max_length=200,null=TRUE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk' : self.pk})

    def save(self):
            super().save()
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 300:
                output_size = (400,300)
                img.thumbnail(output_size)
                img.save(self.image.path)