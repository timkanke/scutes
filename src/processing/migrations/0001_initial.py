# Generated by Django 4.2.3 on 2023-07-13 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('assigned_to', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('reporter', models.CharField(max_length=100)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('pool_report', models.BooleanField()),
                ('publish', models.BooleanField()),
                ('off_the_record', models.BooleanField()),
                ('redaction_review', models.BooleanField()),
                ('comment', models.TextField(blank=True, max_length=1000)),
                ('body_original', models.TextField(blank=True, null=True)),
                ('body_clean', models.TextField(blank=True, null=True)),
                ('body_redact', models.TextField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processing.batch')),
            ],
        ),
    ]