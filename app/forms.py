from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User

from .models import Customer

class LoginForm(AuthenticationForm):
      username = UsernameField(widget=forms. TextInput(attrs={'autofocus ':'True','class':'form-control'}))
      password = forms. CharField(widget=forms.PasswordInput(attrs=
      {'autocomplete' :'current-password', 'class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):     
      username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True',
      'class':'form-control'}))
      email = forms.EmailField(widget=forms.EmailInput(attrs=
      {'class':'form-control'}))
      password1 = forms.CharField(label='Password', widget=forms. PasswordInput
      (attrs={'class':'form-control'}))
      password2 = forms.CharField(label='Confirm Password', widget=forms.
      PasswordInput(attrs={'class':'form-control'}))

      class Meta:
          model = User
          fields = ['username', 'email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
      old_password = forms. CharField(label='Old Password', widget=forms. PasswordInput(attrs={'autofocus ': 'True', 'autocomplete' :'current-password', 'class':'form-control'}))
      new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete' :'current-password', 'class':'form-control'}))
      new_password2 = forms.CharField(label='Confirm Password', widget=forms. PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control'}))
     
     
class MyPasswordResetForm(PasswordResetForm):
      email = forms. EmailField(widget=forms. EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
      new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=
      {'autocomplete':'current-password', 'class':'form-control'}))
      new_password2 = forms.CharField(label='Confirm New Password', widget=forms. PasswordInput(attrs=
      {'autocomplete': 'current-password', 'class': 'form-control'}))



class CustomerProfileForm(forms.ModelForm):
#     mobile = forms.CharField(
#         label="Mobile",
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=True
#     )

    class Meta:
        model = Customer
        fields = ['name', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if len(mobile) != 10:  # Optional: Check for a specific length, e.g., 10 digits.
            raise forms.ValidationError("Mobile number must be 10 digits long.")
        return mobile