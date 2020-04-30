# Generated by Django 3.0.5 on 2020-04-30 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
        ('accounts', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useremotion',
            name='emotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Emotion'),
        ),
        migrations.AddField(
            model_name='useremotion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.Channel'),
        ),
        migrations.AddField(
            model_name='notification',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='channels',
            field=models.ManyToManyField(blank=True, to='channels.Channel'),
        ),
        migrations.AddField(
            model_name='user',
            name='emotions',
            field=models.ManyToManyField(through='accounts.UserEmotion', to='posts.Emotion'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', related_name='tags', through='accounts.UserTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
