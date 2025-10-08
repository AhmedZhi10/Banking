from .models import CustomUser
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    A serializer for creating new users.
    Handles password hashing.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        # List only the fields needed for registration
        fields = (
            'email', 
            'password', 
            'first_name', 
            'last_name', 
            'national_id', 
            'date_of_birth',
            'mobile_number'
        )

    def create(self, validated_data):
        # We use the custom manager's create_user method to handle password hashing
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'], # We can use email as username
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            national_id=validated_data['national_id'],
            date_of_birth=validated_data.get('date_of_birth'),
            mobile_number=validated_data.get('mobile_number'),
        )
        return user
    
    
 