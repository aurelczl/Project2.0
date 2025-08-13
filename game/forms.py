# game/forms.py
from django import forms
from .models import Player, CharacterClass

class PlayerCreationForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["character_class", "default_image_choice", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["character_class"].queryset = CharacterClass.objects.all()
        self.fields["default_image_choice"].label = "Image par défaut à utiliser"