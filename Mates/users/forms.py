from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'birthdate', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomAutForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Этот аккаунт неактивен', code='inactive')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'nickname', 'birthdate', 'profile_description', 'telegram_url', 'steam_url', 'discord_url', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['birthdate'].widget.attrs['type'] = 'date'