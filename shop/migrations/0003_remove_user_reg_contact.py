# Generated by Django 2.0.7 on 2019-07-30 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_user_reg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_reg',
            name='contact',
        ),
    ]
