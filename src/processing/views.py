from django.db.models.query import QuerySet
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters import FilterSet
from django_filters.views import FilterView

from .models import Batch, Item
from .tables import BatchList, ItemList


class Dashboard(TemplateView):
    template_name = "dashboard.html"


class BatchList(SingleTableView):
    model = Batch
    table_class = BatchList
    template_name = "batch_list.html"
    paginate_by = 10
    context_object_name = 'batch'


class ItemFilter(FilterSet):
    class Meta:
        model = Item
        fields = {'redaction_review': ['exact']}


class ItemList(SingleTableMixin, FilterView):
    model = Item
    table_class = ItemList
    template_name = 'item_list.html'

    context_object_name = 'item'

    filterset_class = ItemFilter

    def get_queryset(self) -> QuerySet[any]:
        return super().get_queryset().filter(batch=self.kwargs['batch'])


class ItemView(TemplateView):
    template_name = "item_view.html"
