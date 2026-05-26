from django import forms
from django.contrib.auth import authenticate

from .models import User
from .utils import normalize_phone, validate_github_url


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(username=email, password=password)

        if email and password and user is None:
            raise forms.ValidationError("Неверный имейл или пароль")

        cleaned_data["user"] = user
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")

    def clean_phone(self):
        normalized_phone = normalize_phone(
            self.cleaned_data.get("phone", "")
        )

        users = User.objects.filter(phone=normalized_phone)

        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)

        if normalized_phone and users.exists():
            raise forms.ValidationError(
                "Пользователь с таким телефоном уже существует."
            )

        return normalized_phone

    def clean_github_url(self):
        return validate_github_url(
            self.cleaned_data.get("github_url", "")
        )
