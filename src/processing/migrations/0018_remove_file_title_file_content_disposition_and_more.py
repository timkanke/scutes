# Generated by Django 4.2.3 on 2023-11-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0017_alter_file_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='title',
        ),
        migrations.AddField(
            model_name='file',
            name='content_disposition',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='content_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='content_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
