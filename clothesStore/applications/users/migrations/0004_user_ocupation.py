# Generated by Django 4.1.6 on 2023-03-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_code_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ocupation',
            field=models.CharField(choices=[('0', 'Administrador'), ('1', 'Worker'), ('2', 'Client')], default='2', max_length=1),
        ),
    ]
