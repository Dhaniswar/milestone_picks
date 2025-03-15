from django.db import models
from milestone_picks.s3_setup import AWSSignedURL


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hero_images/')
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
    
    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(
                key=self.image.name
            ),
        }
    

class SportCategory(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='sport_icons/')
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
    
    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(
                key=self.icon.name
            ),
        }


class ContactUs(models.Model):
    full_name = models.CharField(max_length=256, null=True, blank=False, default=None)
    email = models.EmailField(unique=True, null=True, blank=False, default=None)
    phone = models.CharField(max_length=18, unique=True, null=True, blank=True, default=None)
    message = models.TextField(null=True, blank=True, default=None)
    
    class Meta:
        ordering = ['-id']
    
    
    def __str__(self):
        return f'{self.full_name} and {self.message}'



