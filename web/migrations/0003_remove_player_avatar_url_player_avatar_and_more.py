# Generated by Django 5.1.7 on 2025-03-20 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_matchlog_match_alter_matchlog_player_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='avatar_url',
        ),
        migrations.AddField(
            model_name='player',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.png', null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='player',
            name='role',
            field=models.CharField(choices=[('Premium', 'Premium'), ('Normal', 'Normal')], default='Normal', max_length=10),
        ),
    ]
