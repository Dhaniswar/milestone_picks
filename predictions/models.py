from django.db import models
from django.conf import settings
from milestone_picks.s3_setup import AWSSignedURL

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='sport_icons/', blank=True, null=True) 

    def __str__(self):
        return self.name
    
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

    def __str__(self):
        return f"{self.team_1} vs {self.team_2} - {self.match_date}"

class Bet(models.Model):
    BET_TYPES = [
        ('WIN', 'Win'),
        ('LOSE', 'Lose'),
        ('OVER_UNDER', 'Over/Under'),
        ('HANDICAP', 'Handicap'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=20, choices=BET_TYPES)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('WON', 'Won'), ('LOST', 'Lost')], default='PENDING')

    def __str__(self):
        return f"{self.user} - {self.match} - {self.bet_type} - {self.odds}"
    
    def calculate_payout(self):
        """
        todo
        Calculate the payout for a winning bet.
        """
        if self.result == 'WON':
            return self.amount * self.odds
        return 0  # No payout for lost or pending bets