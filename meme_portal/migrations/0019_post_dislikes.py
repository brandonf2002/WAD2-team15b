# Generated by Django 2.2.6 on 2021-03-30 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_portal', '0018_auto_20210330_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to='meme_portal.UserProfile'),
        ),
    ]
