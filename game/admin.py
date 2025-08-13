from django.contrib import admin
from .models import CharacterClass, Player

@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ("name", "intelligence", "agility", "strength", "magic", "charism", "wisdom", "constitution")
    search_fields = ("name",)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("user", "character_class", "intelligence", "agility", "strength", "magic", "charism", "wisdom", "constitution")
    search_fields = ("user__username",)