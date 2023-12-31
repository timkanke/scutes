import re

from django.db import models


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    datetime_added = models.DateTimeField(auto_now=True, null=True)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.CharField(max_length=255, blank=True, null=True)
    content_disposition = models.CharField(max_length=255, blank=True, null=True)
    content_id = models.CharField(max_length=255, blank=True, null=True)
    disposition = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='files')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    @property
    def file_type(self):
        file_type = re.split(';', self.content_type)[0]
        if file_type == 'image/jpeg':
            return 'image'
        if file_type == 'image/jpg':
            return 'image'
        if file_type == 'image/png':
            return 'image'
        if file_type == 'application/pdf':
            return 'pdf'
        if file_type == 'audio/mpeg':
            return 'audio'
        return 'other'


class Item(models.Model):
    class Status(models.IntegerChoices):
        INACTIVE = 0, 'Not Started'
        ACTIVE = 1, 'In Progress'
        COMPLETE = 2, 'Complete'

    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True)
    reporter = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    pool_report = models.BooleanField(null=False)
    publish = models.BooleanField(null=False)
    off_the_record = models.BooleanField(null=False)
    review_status = models.SmallIntegerField(
        choices=Status.choices, blank=False, default='Unspecified', verbose_name='Editorial Review'
    )
    notes = models.TextField(max_length=1000, blank=True, null=True)
    body_original = models.TextField(blank=True, null=True)
    body_clean = models.TextField(blank=True, null=True)
    body_redact = models.TextField(blank=True, null=True)
    body_final = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    batch = models.ForeignKey(
        'Batch',
        on_delete=models.CASCADE,
    )

    @property
    def attachment_count(self):
        return self.file_set.filter(disposition__contains='attachment').count

    @property
    def inline_count(self):
        return self.file_set.filter(disposition__contains='inline').count


class Redact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    string = models.JSONField(null=True)
