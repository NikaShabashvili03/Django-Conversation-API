# Generated by Django 5.1.2 on 2024-12-16 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_conversation_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='creator',
        ),
    ]