# Generated by Django 4.1.6 on 2023-02-25 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_product_is_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_offer',
            field=models.BooleanField(blank=True, verbose_name='Is offer?'),
        ),
    ]
