# Generated by Django 5.1.1 on 2024-09-22 06:46

import django.db.models.deletion
import myauth.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_alter_useravatar_avatar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='useravatar',
            name='avatar',
            field=models.ImageField(upload_to=myauth.models.avatar_upload_path),
        ),
        migrations.AlterField(
            model_name='useravatar',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL),
        ),
    ]