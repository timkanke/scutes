from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters import FilterSet
from django_filters.views import FilterView

import pickle
from base64 import b64encode, b64decode

from .filters import ItemFilter
from .forms import ItemUpdateForm
from .models import Batch, Item
from .tables import BatchList, ItemList


class Index(TemplateView):
    template_name = 'index.html'


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class BatchList(LoginRequiredMixin, SingleTableView):
    model = Batch
    table_class = BatchList
    template_name = 'batch_list.html'
    paginate_by = 10
    context_object_name = 'batch'


class ItemListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Item
    queryset = Item.objects.all()
    context_object_name = 'item_list'
    table_class = ItemList
    template_name = 'item_list.html'
    paginate_by = 15
    context_object_name = 'item'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)

        # Session key
        key = 'my_qs'

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        self.request.session[key] = b64encode(pickle.dumps(self.filterset.qs.query)).decode('ascii')

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['form'] = self.filterset.form
        return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'item_view.html'
    model = Item
    form_class = ItemUpdateForm
    context_object_name = 'item'

    # form_class = ItemUpdateForm
    # object_list = 'item'

    # Form
    def get_success_url(self):
        return reverse('itemupdateview', kwargs={'pk': self.object.pk})

    # Form
    def post(self, request, *args, **kwargs):
        object_list = self.get_object_list()

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
                        pk = (
                            object_list.filter(id__gt=self.object.id)
                            .order_by('id')
                            .only('id')
                            .first()
                        )
                        return redirect('itemupdateview', pk=pk.id)
                    elif 'reset' in request.POST:
                        return HttpResponseRedirect(
                            reverse('itemupdateview', kwargs={'pk': self.object.pk})
                        )
            else:
                return self.form_invalid(form)

    # Form
    def form_valid(self, form):
        return super().form_valid(form)

    # Add info to the form
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return kwargs

    # Navigation
    def get_next_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = (
            object_list.filter(id__gt=current_object_id)
            .order_by('id')
            .only('id')
            .first()
        )
        if qs:
            return qs.id
        else:
            return None

    # Navigation
    def get_previous_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = (
            object_list.filter(id__lt=current_object_id)
            .order_by('-id')
            .only('id')
            .first()
        )
        if qs:
            return qs.id
        else:
            return None

    def get_object_list(self, **kwargs):
        # Session key
        key = 'my_qs'

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        query = pickle.loads(b64decode(self.request.session[key]))
        qs = Item.objects.all()
        qs.query = query

        object_list = qs.order_by('id')
        return object_list

    def query_filter_url(self):
        object_list = self.get_object_list()

        # query_filter_url = self.kwargs['parameter']
        # query_filter_url = QueryDict(mutable=True)  # returns empty dict
        # query_filter_url = dict(self.request.GET)  # returns empty dict, expected since it would be getting url

        query_filter_url = urlencode(
            {'review_status': '2'}
        )  # Desired, however not hardcoded

        return query_filter_url

    # Create context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_object_id = self.object.id
        next_object_id = self.get_next_id(current_object_id)
        previous_object_id = self.get_previous_id(current_object_id)
        object_list = self.get_object_list()
        query_filter_url = self.query_filter_url()

        context['current_object_id'] = current_object_id
        context['next_object_id'] = next_object_id
        context['previous_object_id'] = previous_object_id
        context['object_list'] = object_list
        context['query_filter_url'] = query_filter_url

        try:  # If we have pk, create object with that pk
            pk = self.kwargs['pk']
            instances = Item.objects.filter(pk=pk)
            if instances:
                kwargs['object'] = instances[0]
        except Exception as e:
            pass  # No pk, so no detail
        return context
