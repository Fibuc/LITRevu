# Generated by Django 5.0.6 on 2024-06-26 11:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_follows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
        migrations.CreateModel(
            name='UserFollows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_relations', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur suivi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_relations', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name_plural': 'Follows',
                'unique_together': {('user', 'followed_user')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(blank=True, related_name='followers', through='authentication.UserFollows', to=settings.AUTH_USER_MODEL),
        ),
    ]
