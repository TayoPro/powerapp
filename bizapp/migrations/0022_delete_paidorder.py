# Generated by Django 3.2.7 on 2021-09-20 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizapp', '0021_paidorder'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaidOrder',
        ),
    ]