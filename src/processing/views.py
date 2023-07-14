from django.shortcuts import render
from django.views.generic.base import TemplateView


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class BatchList(TemplateView):
    template_name = "batch_list.html"


class ItemList(TemplateView):
    template_name = "item_list.html"


class ItemView(TemplateView):
    template_name = "item_view.html"
