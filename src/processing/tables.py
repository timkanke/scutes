from django_tables2 import Column, tables, TemplateColumn
from .models import Batch, File, Item


class BatchList(tables.Table):
    class Meta:
        model = Batch
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {'class': 'table table-sm'}
        fields = ['id', 'name', 'assigned_to']

    review = TemplateColumn(template_name='tables/view_item_list.html', orderable=False)
    assigned_to = Column(attrs={'th': {'class': 'text-decoration-line-through text-muted'}}, orderable=False)
    id = Column(verbose_name='ID')
    name = Column(verbose_name='Batch Name')
    finalize = TemplateColumn(verbose_name='', template_name='tables/finalize.html', orderable=False)
