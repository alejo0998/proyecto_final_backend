# Generated by Django 4.0.6 on 2022-10-06 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aprendizaje', '0003_videosena'),
    ]

    operations = [
        migrations.AddField(
            model_name='sena',
            name='permite_signa',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='videosena',
            name='video',
            field=models.FileField(null=True, upload_to='media'),
        ),
    ]
