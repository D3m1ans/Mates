from django.contrib import admin
from .models import Game, UserLibrary

# Register your models here.


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'genre', 'publisher', 'platform', 'release_data')
    search_fields = ('title', 'genre', 'platform',)

@admin.register(UserLibrary)
class UserLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'playtime_hours', 'rating', 'last_played', 'added_at')
    list_filter = ('user', 'game')
    search_fields = ('user__email', 'game__title')
