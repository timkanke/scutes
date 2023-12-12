from django.contrib import admin

from .models import Batch, File, Item, Redact


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'content_disposition', 'disposition', 'content_id', 'item']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'reporter', 'title']


@admin.register(Redact)
class RedactAdmin(admin.ModelAdmin):
    list_display = ['id', 'string']
