from django_tables2 import tables, TemplateColumn
from .models import Batch, Item


class BatchList(tables.Table):
    class Meta:
        model = Batch
        template_name = "django_tables2/bootstrap5.html"
        attrs = {'class': 'table table-sm'}
        fields = ['id',
                  'name',
                  'assigned_to']

    review = TemplateColumn(template_name='tables/view_item_list.html')


class ItemList(tables.Table):
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap5.html"
        attrs = {'class': 'table table-sm'}
        fields = ['id',
                  'date',
                  'reporter',
                  'title',
                  'publish',
                  'review_status']

    review = TemplateColumn(template_name='tables/view_item.html')
