from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

class Country(models.Model):
    """
    Represents a country entity with a unique name. Used as a foreign key in other models to associate related information with a country.
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('name', 'country') # To prevent duplicate cities in the same country

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class CustomUser(AbstractUser):
    # We will use the default first_name, last_name, email from AbstractUser
    # We remove username uniqueness to allow login with email
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    national_id = models.CharField(max_length=14, unique=True,null=True, blank=True )
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    # We tell Django to use the email field as the username for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 'username' is still required for createsuperuser

    def __str__(self):
        return self.email
    
    
    def clean(self):
        super().clean()
        if not self.is_superuser:
            if not self.national_id:
                raise ValidationError("National ID is required for normal users.") 
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.user.email}'s address"