# Generated by Django 4.2.3 on 2023-11-30 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0015_remove_item_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='processing.item'),
        ),
    ]
