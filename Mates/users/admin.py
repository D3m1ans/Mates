from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import Group
from .models import CustomUser


class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'birthdate', 'profile_description', 'status', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Устанавливаем новый пароль
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm  # Используем кастомную форму

    # Поля для отображения списка пользователей
    list_display = ('email', 'nickname', 'is_staff', 'is_active', 'status')

    # Поля, которые будут отображаться при редактировании пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'birthdate', 'profile_description', 'mates_points', 'status', 'profile_picture')}),
        (_('FeedBack'), {'fields': ('telegram_url', 'steam_url', 'discord_url')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'registration_date')}),
    )

    # Поля для добавления пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )

    # Используем нашу кастомную модель пользователя
    model = CustomUser

    search_fields = ('email', 'nickname')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
