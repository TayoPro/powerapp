# Generated by Django 3.2.7 on 2021-09-06 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'managed': True, 'verbose_name': 'Category', 'verbose_name_plural': 'Categoryies'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'managed': True, 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelTable(
            name='category',
            table='category',
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
    ]
