# Generated by Django 4.0.6 on 2022-08-14 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_tokengoogle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='token_google',
        ),
    ]
