from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# class NewClimbForm(forms.Form):
#     # mountains = Mountain.objects.values_list('name', flat=True)
#     mountains = Mountain.objects.all()
#     mountain_list = [mountains.name for mountains.name in mountains]
#     select_a_Mountain = forms.Select(choices=(mountain_list))
#     route_climbed = forms.CharField(max_length=50)
#     date_climbed = forms.DateField()


# class UserCreateForm(UserCreationForm):
#     email = forms.EmailField(required=True,
#                          label='Email',
#                          error_messages={'exists': 'Oops'})

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")


#     def save(self, commit=True):
#         user = super(UserCreateForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user

#     def clean_email(self):
#         if User.objects.filter(email=self.cleaned_data['email']).exists():
#             raise ValidationError(self.fields['email'].error_messages['exists'])
#         return self.cleaned_data['email']
