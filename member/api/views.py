
from rest_framework.generics import CreateAPIView
from .serializers import RegistrationSerializer

class Register(CreateAPIView):
    """
        Provides the possibility of registration
    """
    serializer_class = RegistrationSerializer
