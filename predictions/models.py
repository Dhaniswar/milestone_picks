from django.db import models
from django.conf import settings
from milestone_picks.s3_setup import AWSSignedURL
from django.core.validators import MinValueValidator, MaxValueValidator


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to="sport_icons/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(key=self.icon.name),
        }

    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(key=self.icon.name),
        }


class Match(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.match_date}"


class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    prediction_type = models.CharField(
        max_length=20,
        choices=[
            ("WIN", "Win"),
            ("LOSE", "Lose"),
            ("OVER_UNDER", "Over/Under"),
            ("HANDICAP", "Handicap"),
            ("OTHER", "Other"),
        ],
    )
    our_prediction = models.CharField(
        max_length=225,
        blank=True,
        null=True,
        help_text="Our formatted prediction, e.g., 'Boston Celtics -5.5'",
    )
    confidence_level = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Confidence level from 0.0 to 5.0",
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    predicted_outcome = models.CharField(
        max_length=100,
        help_text="The predicted outcome, e.g., 'Team 1 wins' or 'Over 2.5 goals'",
    )
    actual_outcome = models.CharField(
        max_length=100, blank=True, null=True, help_text="What actually happened"
    )
    placed_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("CORRECT", "Correct"),
            ("INCORRECT", "Incorrect"),
        ],
        default="PENDING",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.match} - {self.prediction_type}"

    def save(self, *args, **kwargs):
        # Automatically set result if actual_outcome is provided
        if self.actual_outcome:
            if self.predicted_outcome == self.actual_outcome:
                self.result = "CORRECT"
            else:
                self.result = "INCORRECT"
        super().save(*args, **kwargs)
