# Generated by Django 4.0.6 on 2022-08-14 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_usuario_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='token',
            new_name='token_google',
        ),
    ]
