# Generated by Django 2.2.24 on 2021-11-24 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20211124_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='matches',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='whoLikeMe',
            field=models.TextField(blank=True, default=''),
        ),
    ]