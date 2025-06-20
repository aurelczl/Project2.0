# Generated by Django 5.1.7 on 2025-06-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_remove_book_read_book_statut'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='stop_area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='manga',
            name='statut',
            field=models.CharField(blank=True, choices=[('Fini', 'Fini'), ('Arrêté', 'Arrêté'), ('En cours', 'En cours'), ('En attente', 'En attente')], max_length=10, null=True),
        ),
    ]
