# Generated by Django 4.2 on 2024-07-12 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0006_systemcomponent_serial_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system',
            name='components',
        ),
    ]