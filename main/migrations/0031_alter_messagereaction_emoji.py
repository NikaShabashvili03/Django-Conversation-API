# Generated by Django 5.1.2 on 2024-12-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_conversation_lastmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagereaction',
            name='emoji',
            field=models.CharField(max_length=2),
        ),
    ]