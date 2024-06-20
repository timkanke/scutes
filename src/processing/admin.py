from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import path, reverse
from django.views.generic.detail import DetailView

import csv

from .models import Batch, File, Item, User
from processing.common.clean import clean
from processing.common.mark_redaction import mark_redaction


admin.site.register(User, UserAdmin)
admin.site.site_header = 'Scutes Admin'
admin.site.site_title = 'Scutes Admin'

@admin.action
def export_to_csv(self, request, queryset):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mymodel.csv"'
    # Create the CSV writer
    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Field1', 'Field2', 'Field3'])
    # Write the data rows
    for obj in queryset:
        writer.writerow([obj.id, obj.name, obj.datetime_added])
    # Return the response
    return response


class BatchDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "processing.view_batch"
    template_name = "admin/processing/batch/detail.html"
    model = Batch

    def get_context_data(self, **kwargs):
        
        return {
            **super().get_context_data(**kwargs),
            **admin.site.each_context(self.request),
            "opts": self.model._meta,
        }


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'datetime_added', 'last_export', 'detail']
    list_filter = ['datetime_added', 'last_export']
    search_fields = ['name']
    actions = [export_to_csv]

    def get_urls(self):
        return [
            path("<pk>/detail", self.admin_site.admin_view(BatchDetailView.as_view()), name=f"processing_batch_detail",),
            *super().get_urls(), 
        ]

    def detail(self, obj: Batch) -> str:
        url = reverse("admin:processing_batch_detail", args=[obj.pk])
        return format_html(f'<a href="{url}">Open</a>')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'content_disposition', 'disposition', 'content_id', 'item']
    list_filter = ['disposition']
    actions = [export_to_csv]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'reporter', 'title', 'publish']
    list_filter = ['publish']
    search_fields = ['reporter', 'title']
    actions = [export_to_csv]
    
