# Generated by Django 4.2.3 on 2024-05-08 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("processing", "0006_alter_batch_assigned_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batch",
            name="assigned_to",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]