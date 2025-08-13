from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.value}"

class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    intelligence = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    magic = models.IntegerField(default=0)
    charism = models.IntegerField(default=0)
    wisdom = models.IntegerField(default=0)
    constitution = models.IntegerField(default=0)
    default_image_male = models.ImageField(upload_to='character_classes/male/', blank=True, null=True)
    default_image_female = models.ImageField(upload_to='character_classes/male/', blank=True, null=True)

    def __str__(self):
        return self.name
        
class Player(models.Model):

    IMAGE_CHOICES = (
        ('M', 'MaleIm'),
        ('F', 'FemaleIm'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    intelligence = models.IntegerField(default=0, help_text="Intelligence score")
    agility = models.IntegerField(default=0, help_text="Agility score")
    strength = models.IntegerField(default=0, help_text="Strength score")
    magic = models.IntegerField(default=0, help_text="Magic score")
    charism = models.IntegerField(default=0, help_text="charism score")
    wisdom = models.IntegerField(default=0)
    constitution = models.IntegerField(default=0)
    
    # Choix de l'image par défaut à utiliser parmi celles de la classe
    default_image_choice = models.CharField(max_length=1, choices=IMAGE_CHOICES, default='M')
    
    # Image personnalisée facultative
    image = models.ImageField(upload_to='player_images/', blank=True, null=True)

    @property
    def displayed_image(self):
        # Priorité à l'image personnalisée si elle existe
        if self.image:
            return self.image.url
        
        # Sinon on prend l'image de la classe selon le choix du joueur
        if self.character_class:
            if self.default_image_choice == 'M' and self.character_class.default_image_male:
                return self.character_class.default_image_male.url
            elif self.default_image_choice == 'F' and self.character_class.default_image_female:
                return self.character_class.default_image_female.url
        
        # Pas d'image disponible
        return None

    @property
    def performances(self):
        return {
            "Intelligence": self.intelligence,
            "Magic": self.magic,
            "Charism": self.charism,
            "Agility": self.agility,
            "Strength": self.strength,
            "Wisdom": self.wisdom,
            "Constitution": self.constitution,
        }

    def __str__(self):
        #return f"{self.user.username} - Stats"
        return f"{self.user.username} - {self.character_class.name if self.character_class else 'No class'}"

