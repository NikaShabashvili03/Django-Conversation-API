# Generated by Django 5.1.2 on 2024-12-17 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_conversation_creator_conversation_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='creator',
        ),
    ]