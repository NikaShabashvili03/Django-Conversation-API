# Generated by Django 5.1.2 on 2024-12-17 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_conversation_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='participants',
            new_name='users',
        ),
    ]
