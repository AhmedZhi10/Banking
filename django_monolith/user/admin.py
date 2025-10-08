from django.contrib import admin
from .models import CustomUser, Country, City, Address

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Address)