from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAutForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Этот аккаунт неактивен', code='inactive')
