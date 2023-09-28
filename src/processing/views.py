from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters import FilterSet
from django_filters.views import FilterView

from .forms import ItemUpdateForm
from .models import Batch, Item
from .tables import BatchList, ItemList


class Index(TemplateView):
    template_name = "index.html"


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"


class BatchList(LoginRequiredMixin, SingleTableView):
    model = Batch
    table_class = BatchList
    template_name = "batch_list.html"
    paginate_by = 10
    context_object_name = 'batch'


class ItemFilter(FilterSet):

    class Meta:
        model = Item
        fields = {'reporter': ['contains'],
                  'review_status': ['exact']
                  }


class ItemList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Item
    table_class = ItemList
    template_name = 'item_list.html'
    paginate_by = 15
    context_object_name = 'item'

    filterset_class = ItemFilter


class ItemView(LoginRequiredMixin, MultipleObjectMixin, UpdateView):
    form_class = ItemUpdateForm
    model = Item
    template_name = "item_view.html"
    object_list = 'item'

    def get_success_url(self):
        return reverse('itemview', kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()

        if request.method == 'POST':
            if form.is_valid():
                if self.request.POST:
                    if 'save_add' in request.POST:
                        return self.form_valid(form)
                    elif 'save_continue' in request.POST:
                        self.form_valid(form)
                        return HttpResponseRedirect(reverse('itemview', kwargs={'pk': self.object.pk+1}))
                    elif 'reset' in request.POST:
                        return HttpResponseRedirect(reverse('itemview', kwargs={'pk': self.object.pk}))
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)
