# Generated by Django 5.1.2 on 2024-12-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
