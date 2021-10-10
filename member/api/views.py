from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import RegistrationSerializer, ResetPasswordByEmailSerializer, ContactUsSerializer
from ..models import Customer, ContactUs
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
        send_reset_password_mail(
            subject='درخواست بازیابی رمز عبور',
            message=f' {customer.first_name} عزیز، درخواست شما برای بازیابی رمز عبور دریافت شد. کد تایید شما جهت احراز هویت: {password}',
            recipient_list=[info['email']]
        )  # using multi-threading send the OTP using Email services
        return Response({'email': info['email']}, status=status.HTTP_200_OK)



from rest_framework import mixins
from rest_framework import generics

class Contact_us(mixins.CreateModelMixin,
                    GenericAPIView
    # , generics.GenericAPIView
                 ):
    # queryset = Contact_us.objects.all()
    serializer_class = ContactUsSerializer

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        print("==================================")
        print()
        # ContactUs(name=self.serializer_class.validated_data)
        return HttpResponse(status=201)

# class Contact_us(CreateView):
    # """
    #
    # """
    # model = ContactUs
    # form_class = ContactUsForm
    #
    # def get_success_url(self):
    #     # self.success_url = self.request.path
    #     return redirect('home/')

    # def get_success_url(self):
    #     get_lang = self.request.path.split('/')
    #     print(self.request.path)
    #     return redirect(f'/{get_lang[1]}/home/')