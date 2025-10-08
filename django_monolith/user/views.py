# users/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    An API endpoint for creating a new user.
    This is a public endpoint.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    # Allow any user (authenticated or not) to access this endpoint.
    permission_classes = [AllowAny]
    
       # This is the new protected view
class UserProfileView(generics.RetrieveAPIView):
    """
    An API endpoint to view the logged-in user's profile.
    """
    serializer_class = UserRegistrationSerializer # We can reuse the registration serializer for now
    permission_classes = [IsAuthenticated]     # <-- This is the magic line!

    def get_object(self):
        # This method returns the object that the view will display.
        # We override it to always return the currently logged-in user from the request.
        return self.request.user