# Generated by Django 2.0.7 on 2019-07-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190731_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reg',
            name='contact_info',
            field=models.BigIntegerField(),
        ),
    ]
