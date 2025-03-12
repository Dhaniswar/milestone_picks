from django.db import models
from milestone_picks.s3_setup import AWSSignedURL


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hero_images/')

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

    def __str__(self):
        return self.name
    
    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(
                key=self.icon.name
            ),
        }