# Generated by Django 4.1.1 on 2024-05-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_ui', '0006_role_optional_alter_player_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
