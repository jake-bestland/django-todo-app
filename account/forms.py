from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Email',
                                           'class': 'form-control'}))
    first_name = forms.CharField(required=True,
                                 widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'First Name',
                                           'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Last Name',
                                           'class': 'form-control'}))
    username = forms.CharField(widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Username',
                                           'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(
                                    attrs={'placeholder': 'Password',
                                           'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(
                                    attrs={'placeholder': 'Password Confirmation',
                                           'class': 'form-control'}))

    class Meta:
        fields = ['email',
                  'username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2', ]
        model = Account


class SigninForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Username',
                                           'class': 'form-control'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(
                                    attrs={'placeholder': 'Password',
                                           'class': 'form-control'}))
    

class AccountUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Account
        fields = ('username', 'email', 'profile_image', 'hide_email')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account