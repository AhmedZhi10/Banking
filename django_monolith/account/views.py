# accounts/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Account
# Import both serializers
from .serializers import AccountListSerializer, AccountCreateSerializer

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    
    http_method_names = ['get', 'post', 'head', 'options']

    # This method dynamically selects the serializer based on the action
    def get_serializer_class(self):
        if self.action == 'create':
            return AccountCreateSerializer
        return AccountListSerializer # For 'list', 'retrieve', etc.

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)