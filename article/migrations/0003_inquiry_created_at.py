# Generated by Django 3.1.1 on 2020-09-17 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_inquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='登録日'),
            preserve_default=False,
        ),
    ]
