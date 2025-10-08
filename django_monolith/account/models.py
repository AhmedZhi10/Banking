from django.db import models
from user.models import CustomUser



class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Savings, Checking")
    def __str__(self):
        return self.name


    
class AccountStatus(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Active, Frozen, Closed")

    class Meta:
        verbose_name_plural = "Account Statuses"

    def __str__(self):
        return self.name




class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    status = models.ForeignKey(AccountStatus, on_delete=models.PROTECT)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)