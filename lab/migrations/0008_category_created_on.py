# Generated by Django 4.2 on 2024-05-15 17:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0007_system_lab'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_on',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
