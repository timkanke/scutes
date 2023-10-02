from django_tables2 import Column, tables, TemplateColumn
from .models import Batch, Item


class BatchList(tables.Table):
    class Meta:
        model = Batch
        template_name = "django_tables2/bootstrap5.html"
        attrs = {'class': 'table table-sm'}
        fields = ['id',
                  'name',
                  'assigned_to']

    review = TemplateColumn(template_name='tables/view_item_list.html', orderable=False)
    assigned_to = Column(verbose_name='assigned_to (Under Development)')
    id = Column(verbose_name='ID')
    name = Column(verbose_name='Batch Name')


class ItemList(tables.Table):

    review_status = Column(attrs={'td': {'class': lambda value: 'bg-success' if value == 'Complete'
                                         else ('bg-warning' if value == 'In Progress' else 'bg-danger')}})

    class Meta:
        model = Item
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {'class': 'table table-sm'}
        row_attrs = {
            'review_status': lambda value: value.name
        }
        fields = ['id',
                  'date',
                  'reporter',
                  'title',
                  'publish',
                  'review_status']

    review = TemplateColumn(template_name='tables/view_item.html', orderable=False)
