# Generated by Django 4.2.3 on 2023-07-17 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0004_alter_item_last_modified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='redaction_review',
            new_name='review_status',
        ),
    ]
