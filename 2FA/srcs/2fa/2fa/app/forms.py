from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser
from django_otp.plugins.otp_totp.models import TOTPDevice

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'enable_2fa']
    
    username = forms.CharField(
        label='Username',
        max_length=15,
        help_text="Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )
    enable_2fa = forms.BooleanField(
        label='Enable 2FA',
        required=False,
        help_text="Enable Two-Factor Authentication for added security."
    )

    field_order = ['username', 'password1', 'password2', 'enable_2fa']

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")

        has_uppercase = any(char.isupper() for char in password1)
        has_digit = any(char.isdigit() for char in password1)
        has_special = any(char in "!@#$%^&*()-_=+[]{};:'\"|\\<>,./?" for char in password1)
        
        if not (has_uppercase and has_digit and has_special):
            raise forms.ValidationError("Password must contain at least one uppercase letter, one digit, and one special character.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class Enable2FAForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(Enable2FAForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['verification_code'] = forms.CharField(label='Verification Code', max_length=6)

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        totp_device = TOTPDevice.objects.filter(user=self.user).first()

        if not totp_device or not totp_device.verify_token(code):
            raise forms.ValidationError("Incorrect code.")
        
        return code
