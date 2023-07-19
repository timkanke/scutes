from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import MultipleObjectMixin
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters import FilterSet
from django_filters.views import FilterView

from .forms import ItemUpdateForm
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
        fields = {'review_status': ['exact']}


class ItemList(FilterView, SingleTableMixin):
    model = Item
    table_class = ItemList
    template_name = 'item_list.html'
    paginate_by = 5
    context_object_name = 'item'

    filterset_class = ItemFilter

    def get_queryset(self) -> QuerySet[any]:
        return super().get_queryset().filter(batch=self.kwargs['batch'])


class ItemView(UpdateView, MultipleObjectMixin):
    form_class = ItemUpdateForm
    model = Item
    template_name = "item_view.html"
    success_message = "Saved Succesfully"
    object_list = 'item'

    def get_success_url(self):
        return reverse('itemview', kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)
