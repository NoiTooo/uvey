# Generated by Django 3.1.1 on 2020-09-13 17:42

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', register.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='account_name',
            field=models.CharField(default='tomo', max_length=30, verbose_name='account name'),
            preserve_default=False,
        ),
    ]
