from django.db import models
from milestone_picks.s3_setup import AWSSignedURL

from django.utils.translation import gettext_lazy as _


class AboutSection(models.Model):
    background_image = models.ImageField(upload_to='about/')
    main_title = models.CharField(max_length=100)
    main_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.main_title
    
    def about_background_image(self):
        return {
            "s3_obj": AWSSignedURL.get(key=self.background_image.name),
        }


class Statistic(models.Model):
    SECTION_CHOICES = [
        ('top', 'Top Section'),
        ('bottom', 'Bottom Section'),
    ]

    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    icon = models.CharField(
        max_length=50, help_text="Font awesome or other icon class")
    number = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.number} - {self.description}"


class MissionSection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def mission_section_image(self):
        return {
            "s3_obj": AWSSignedURL.get(key=self.image.name),
        }


class WhyChooseUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Why Choose Us"

    def __str__(self):
        return self.title


class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class BettingPhilosophy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Betting Philosophies"

    def __str__(self):
        return self.title

    def betting_philosophy_image(self):
        return {
            "s3_obj": AWSSignedURL.get(key=self.image.name),
        }




class ValueProposition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ValueItem(models.Model):
    proposition = models.ForeignKey(
        ValueProposition, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.proposition.title} - {self.title}"


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.CharField(max_length=50)
    background_image = models.ImageField(upload_to='about/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Testimonial by {self.author}"


class CallToAction(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    contact_text = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Call to Action"

    def __str__(self):
        return self.title
