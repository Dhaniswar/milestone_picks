from django.db import models
from django.conf import settings
from milestone_picks.s3_setup import AWSSignedURL

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='sport_icons/', blank=True, null=True)
    
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

    def sport_icon(self):
        return {
            "s3_obj": AWSSignedURL.get(
                key=self.icon.name
            ),
        }

class Match(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    match_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.match_date}"

class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    prediction_type = models.CharField(max_length=20, choices=[
        ('WIN', 'Win'),
        ('LOSE', 'Lose'),
        ('OVER_UNDER', 'Over/Under'),
        ('HANDICAP', 'Handicap'),
        ('OTHER', 'Other'),
    ])
    predicted_outcome = models.CharField(max_length=100, help_text="The predicted outcome, e.g., 'Team 1 wins' or 'Over 2.5 goals'")
    placed_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('CORRECT', 'Correct'), ('INCORRECT', 'Incorrect')], default='PENDING')
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user} - {self.match} - {self.prediction_type}"