# from dj_rest_auth.views import LoginView
from rest_framework import serializers
from member.models import Customer

class RegistrationSerializer(serializers.ModelSerializer):
    password_Confirmation = serializers.CharField(write_only=True, style={
            'input_type': 'password'
        })

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'password_Confirmation', ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        new_customer = Customer(
            username=self._validated_data['username'],
            email=self._validated_data['email'],
        )
        password = self.validated_data['password']
        password_Confirmation = self.validated_data['password_Confirmation']

        if password != password_Confirmation:
            raise serializers.ValidationError({
                'password': _('Passwords must match'),
            })

        elif len(password) < 8:
            raise serializers.ValidationError({
                'password': _('Your password must be at least 8 characters long.')
            })

        new_customer.set_password(password)
        new_customer.save()

        return new_customer