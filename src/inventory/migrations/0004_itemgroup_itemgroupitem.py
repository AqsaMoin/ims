# Generated by Django 4.2 on 2025-03-03 03:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('inventory', '0003_alter_system_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_group_name', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.department')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.organisation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.room')),
            ],
        ),
        migrations.CreateModel(
            name='ItemGroupItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('item_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.itemgroup')),
            ],
            options={
                'unique_together': {('item_group', 'item')},
            },
        ),
    ]
