from django import forms
from django.contrib.auth.models import User
from . models import Profile
from django.core.exceptions import ValidationError

class User_RegistrationForm(forms.Form) :

    user_name = forms.CharField(min_length=1,max_length=50,label='User name ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your user name'}))
    first_name = forms.CharField(min_length=1,max_length=50,label='First name ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your first name'}))
    last_name = forms.CharField(min_length=1,max_length=50,label='Last name ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your last name'}))
    email = forms.EmailField(label='Email ',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Your email'}))
    first_password = forms.CharField(max_length=20,label='Password ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}))
    second_password = forms.CharField(max_length=20,label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm your password'}))

    def clean_user_name(self) :
        user_name = self.cleaned_data['user_name']
        user = User.objects.filter(username=user_name).exists()
        if user :
            raise ValidationError('This user name has already taken , try a new one')
        return user_name

    def clean_email(self) :
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user :
            raise ValidationError('This email has already taken , try a new one')
        return email

    def clean(self):
        cd = super().clean()
        password = cd.get('first_password')
        confirm_password = cd.get('second_password')
        if password and confirm_password and password != confirm_password :
            raise ValidationError('Passwords do not match , check them please')
class User_LoginForm(forms.Form) :

    user_name_or_email = forms.CharField(label='User name / Email ',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your user name or email'}))
    password = forms.CharField(max_length=20,label='Password ',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your password'}))

class User_ChangeForm(forms.ModelForm) :

    email = forms.EmailField(label='Email ',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your new email'}))

    class Meta :
        model = Profile
        fields = ('user_age','user_bio')
        widgets = {
            'user_age' : forms.NumberInput(attrs={'class':'form-control'}),
            'user_bio' : forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your new biography'}),
        }