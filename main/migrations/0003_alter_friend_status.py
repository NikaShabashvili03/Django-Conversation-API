# Generated by Django 5.1.2 on 2024-12-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_friend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending', max_length=10),
        ),
    ]
