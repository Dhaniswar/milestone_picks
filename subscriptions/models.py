from django.conf import settings
from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)  # e.g., Weekly, Monthly, Yearly
    stripe_plan_id = models.CharField(max_length=100)  # Stripe plan ID
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price in USD
    duration = models.CharField(max_length=20)  # e.g., "1 week", "1 month", "1 year"
    
    class Meta:
        ordering = ['-id']
        

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100)  # Stripe subscription ID
    status = models.CharField(max_length=20, default="active")  # e.g., "active", "canceled"
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-id']
        

    def __str__(self):
        return f"{self.user} - {self.plan}"