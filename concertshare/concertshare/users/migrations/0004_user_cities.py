# Generated by Django 2.0.6 on 2018-06-29 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_date_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cities',
            field=models.CharField(default='San Francisco', max_length=255, verbose_name='Cities'),
        ),
    ]
