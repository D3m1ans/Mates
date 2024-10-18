from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'birthdate', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Пароль шифруется с помощью метода set_password
        if commit:
            user.save()  # Сохраняем пользователя в базу данных
        return user

class CustomAutForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Этот аккаунт неактивен', code='inactive')
