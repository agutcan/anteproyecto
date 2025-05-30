# Generated by Django 5.2 on 2025-04-26 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_tournament_matches_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team1_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='team1_winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='team2_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='match',
            name='team2_winner',
            field=models.BooleanField(default=False),
        ),
    ]
