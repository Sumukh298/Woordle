from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username) < 5:
            raise forms.ValidationError(
                "Username must be at least 5 characters long."
            )

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if password:
            if len(password) < 5:
                raise forms.ValidationError(
                    "Password must be at least 5 characters long."
                )

            if not any(char.isalpha() for char in password):
                raise forms.ValidationError(
                    "Password must contain a letter."
                )

            if not any(char.isdigit() for char in password):
                raise forms.ValidationError(
                    "Password must contain a number."
                )

            if not any(char in "$%*&" for char in password):
                raise forms.ValidationError(
                    "Password must contain one of $, %, *, or &."
                )

        return cleaned_data