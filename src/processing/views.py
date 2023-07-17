from django.shortcuts import render
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableView

from .models import Batch
from .tables import BatchList


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class BatchList(SingleTableView):
    model = Batch
    table_class = BatchList
    template_name = "batch_list.html"
    paginate_by = 10
    context_object_name = 'batch'


class ItemList(TemplateView):
    template_name = "item_list.html"


class ItemView(TemplateView):
    template_name = "item_view.html"
