from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from urllib.parse import urlparse

from .models import User


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
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return phone

        if phone.startswith("8") and len(phone) == 11 and phone.isdigit():
            normalized_phone = "+7" + phone[1:]
        elif phone.startswith("+7") and len(phone) == 12 and phone[1:].isdigit():
            normalized_phone = phone
        else:
            raise forms.ValidationError(
                "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
            )

        users = User.objects.filter(phone=normalized_phone)

        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)

        if users.exists():
            raise forms.ValidationError("Пользователь с таким телефоном уже существует.")

        return normalized_phone

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url", "").strip()

        if not github_url:
            return github_url

        parsed_url = urlparse(github_url)

        if parsed_url.netloc not in ("github.com", "www.github.com"):
            raise forms.ValidationError("Ссылка должна вести на GitHub.")

        return github_url

class CustomPasswordChangeForm(PasswordChangeForm):
    pass