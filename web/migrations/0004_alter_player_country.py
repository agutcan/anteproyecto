# Generated by Django 5.1.7 on 2025-03-21 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_player_avatar_url_player_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brasil'), ('CL', 'Chile'), ('CO', 'Colombia'), ('ES', 'España'), ('MX', 'México'), ('US', 'Estados Unidos')], default='ES', max_length=2),
        ),
    ]
