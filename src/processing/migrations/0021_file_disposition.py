# Generated by Django 4.2.3 on 2023-12-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0020_rename_file_content_disposition_file_content_disposition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='disposition',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
