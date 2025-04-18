from django.db import models

from django.utils.text import slugify


class BettingInfoSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ("hero", "Hero Section"),
        ("text_image", "Text with Image"),
        ("image_text", "Image with Text"),
    ]

    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to="betting_info/", blank=True, null=True)
    section_type = models.CharField(max_length=20, choices=SECTION_TYPE_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Betting Info Section"
        verbose_name_plural = "Betting Info Sections"

    def __str__(self):
        return f"{self.get_section_type_display()} - {self.title or 'No Title'}"


class BettingTip(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="betting_tips/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Betting Tip"
        verbose_name_plural = "Betting Tips"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BettingBasicConcept(models.Model):
    CONCEPT_TYPE_CHOICES = [
        ("point_spreads", "Point Spreads"),
        ("moneylines", "Moneylines"),
        ("totals", "Totals (Over/Under)"),
        ("prop_bets", "Prop Bets"),
        ("parlays", "Parlays"),
        ("teasers", "Teasers"),
    ]

    title = models.CharField(max_length=100)
    concept_type = models.CharField(max_length=20, choices=CONCEPT_TYPE_CHOICES)
    description = models.TextField()
    example = models.TextField()
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Font Awesome icon class or similar",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Betting Basic Concept"
        verbose_name_plural = "Betting Basic Concepts"

    def __str__(self):
        return f"{self.get_concept_type_display()} - {self.title}"
