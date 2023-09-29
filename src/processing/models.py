from django.db import models


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    datetime_added = models.DateTimeField(auto_now=True, null=True)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True)
    reporter = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    pool_report = models.BooleanField(null=False)
    publish = models.BooleanField(null=False)
    off_the_record = models.BooleanField(null=False)
    review_status = models.CharField(max_length=255, blank=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    body_original = models.TextField(blank=True, null=True)
    body_clean = models.TextField(blank=True, null=True)
    body_redact = models.TextField(blank=True, null=True)
    body_final = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    batch = models.ForeignKey(
        "Batch",
        on_delete=models.CASCADE,
    )


class Redact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    string = models.JSONField(null=True)
