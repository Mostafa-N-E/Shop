from django import forms
from member.models import Customer, ContactUs


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True
        self.fields['gender'].disabled = True

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'gender', 'address',
                  'postal_code', 'city', ]


# class ContactUsForm(forms.ModelForm):
#     class Meta:
#         model = ContactUs
#         fields = ['name', 'subject', 'email', 'message', ]
