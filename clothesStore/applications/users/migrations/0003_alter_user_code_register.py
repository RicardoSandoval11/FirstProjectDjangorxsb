# Generated by Django 4.1.6 on 2023-02-14 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_code_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code_register',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Register code'),
        ),
    ]