from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from .serializers import RegistrationSerializer, ResetPasswordByEmailSerializer, ContactUsSerializer
from ..models import Customer
from djangoShop.utils import send_reset_password_mail
import secrets
import string



class Register(CreateAPIView):
    """
        Provides the possibility of registration
    """
    serializer_class = RegistrationSerializer


class RequestResetPasswordEmail(APIView):
    """
        Enable users to recover passwords via email with this view
    """
    def post(self, request):
        try:
            customer = Customer.objects.get(email=request.data['email'])
        except Customer.DoesNotExist:
            return Response({'customer': ['کاربری با مشخصات داده‌شده پیدا نشد']}, status=status.HTTP_404_NOT_FOUND)

        serializer = ResetPasswordByEmailSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        info = serializer.validated_data
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))  # generated password (8-character)
        customer.set_password(password)
        customer.save()
        send_reset_password_mail(
            subject='درخواست بازیابی رمز عبور',
            message=f' {customer.first_name} عزیز، درخواست شما برای بازیابی رمز عبور دریافت شد. کد تایید شما جهت احراز هویت: {password}',
            recipient_list=[info['email']]
        )  # using multi-threading send the OTP using Email services
        return Response({'email': info['email']}, status=status.HTTP_200_OK)


class Contact_us(mixins.CreateModelMixin, GenericAPIView):
    """
        Record messages sent by users through the contact form
    """
    serializer_class = ContactUsSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return HttpResponse(status=201)
