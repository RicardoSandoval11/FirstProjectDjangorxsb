# Generated by Django 4.1.6 on 2023-02-14 04:29

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_carshop'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carshop',
            options={'ordering': ['-created'], 'verbose_name': 'Car shop', 'verbose_name_plural': 'Car shop'},
        ),
        migrations.AddField(
            model_name='carshop',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='carshop',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
    ]
