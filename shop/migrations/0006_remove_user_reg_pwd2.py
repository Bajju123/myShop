# Generated by Django 2.0.7 on 2019-07-30 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20190731_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_reg',
            name='pwd2',
        ),
    ]
