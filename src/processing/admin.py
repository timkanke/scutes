from django.contrib import admin

from .models import Batch, Item, RedactedStrings


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'reporter', 'title']


@admin.register(RedactedStrings)
class RedactedStringsAdmin(admin.ModelAdmin):
    list_display = ['id', 'string']
