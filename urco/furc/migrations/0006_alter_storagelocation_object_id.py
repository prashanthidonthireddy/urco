# Generated by Django 4.2.16 on 2024-09-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furc', '0005_storagelocation_object_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagelocation',
            name='object_id',
            field=models.CharField(max_length=10),
        ),
    ]
