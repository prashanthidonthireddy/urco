# Generated by Django 4.2.16 on 2024-09-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furc', '0010_order_updated_date_alter_order_order_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Received', 'Received'), ('Approved by supervisor', 'Approved by supervisor'), ('Stored', 'Stored'), ('Closed', 'Closed'), ('Delivered', 'Delivered'), ('Approved by higher', 'Approved by higher'), ('Ordered', 'Ordered'), ('Requested', 'Requested'), ('rejected', 'rejected'), ('Pending higher approval', 'Pending higher approval'), ('Pending approval', 'Pending approval'), ('Order in progress', 'Order in progress')], default='Requested', max_length=30),
        ),
    ]
