# Generated by Django 4.2.3 on 2023-08-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0007_redact_delete_redactedstrings'),
    ]

    operations = [
        migrations.AddField(
            model_name='redact',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]
