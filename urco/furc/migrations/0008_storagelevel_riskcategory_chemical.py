# Generated by Django 4.2.16 on 2024-09-22 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('furc', '0007_rename_object_id_storagelocation_location_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='StorageLevel',
            fields=[
                ('storage_level_id', models.IntegerField(primary_key=True, serialize=False)),
                ('storage_level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RiskCategory',
            fields=[
                ('risk_category_id', models.IntegerField(primary_key=True, serialize=False)),
                ('risk_category', models.CharField(max_length=20)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furc.userrole')),
            ],
        ),
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('chemical_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=50)),
                ('systematic_name', models.CharField(max_length=50)),
                ('risk_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='furc.riskcategory')),
            ],
        ),
    ]
