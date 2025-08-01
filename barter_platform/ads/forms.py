from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from ads.models import Ad, ExchangeProposal
from django.contrib.auth.models import User


class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ExchangeForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)

        self.fields['ad_receiver'].queryset = Ad.objects.exclude(user=user)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class AuthForm(UserCreationForm):
    username = forms.CharField(required=True, label='Имя пользователя')
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Подтвердите пароль',
                                widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):
    username = forms.CharField(required=True, label='Имя пользователя')
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password']





