# Generated by Django 2.0.7 on 2019-08-02 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20190802_1825'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='product_n',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='product_n',
            name='category',
        ),
        migrations.DeleteModel(
            name='Product_N',
        ),
    ]
