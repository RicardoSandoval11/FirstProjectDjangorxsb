# Generated by Django 4.1.6 on 2023-02-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_carshop_amout_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carshop',
            name='total_amount',
            field=models.FloatField(verbose_name='Amount'),
        ),
    ]
