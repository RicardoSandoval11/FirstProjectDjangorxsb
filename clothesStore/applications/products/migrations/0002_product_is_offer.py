# Generated by Django 4.1.6 on 2023-02-10 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_offer',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is offer?'),
        ),
    ]