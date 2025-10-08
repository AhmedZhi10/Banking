# accounts/serializers.py

from rest_framework import serializers
from .models import Account,AccountStatus,AccountType

class AccountListSerializer(serializers.ModelSerializer):
    """Serializer for listing/retrieving accounts (read-only)."""
    # These fields are for display purposes.
    account_type = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = [
            'id', 
            'user',
            'account_number', 
            'balance', 
            'account_type', 
            'status', 
            'created_at'
        ]

class AccountCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating accounts (write-only)."""
    class Meta:
        model = Account
        # We only need the user to provide these fields.
        # The 'user' field will be added automatically from the view.
        fields = ['account_number', 'account_type', 'status']

