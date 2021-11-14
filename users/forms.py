import hashlib
import random

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core.mail import send_mail
from django.urls import reverse

from users.models import User, UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self):
        user = super(UserRegistrationForm, self).save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1(str(user.email + salt).encode('utf8')).hexdigest()
        user.save()
        self.send_verify_mail(user)
        return user

    @staticmethod
    def send_verify_mail(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])

        title = f'Поддтверждение учетной записи {user.username}'

        message = f'Для подтверждения учетной записи {user.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    current_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    hometown = forms.CharField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    age = forms.CharField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('hometown', 'current_city', 'gender')

        def __init__(self, *args, **kwargs):
            super(UserProfileEditForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''
