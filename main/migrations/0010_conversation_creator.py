# Generated by Django 5.1.2 on 2024-12-17 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_conversation_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='creator',
            field=models.ManyToManyField(related_name='initiated_conversations', to='main.user'),
        ),
    ]
