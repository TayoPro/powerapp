# Generated by Django 3.2.7 on 2021-09-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizapp', '0012_profiledetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='max_quantity',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='product',
            name='min_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
