from rest_framework import serializers
from .models import Score

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'user', 'value', 'created_at']
        read_only_fields = ['user', 'created_at']
