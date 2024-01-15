from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import management
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, UpdateView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin, SingleTableView

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

    def run_management_command(self, object_id):
        batch_number = 1
        run_mark_redaction = management.call_command('mark_redaction', batch_number)
        return run_mark_redaction

    def get_context_data(self, **kwargs):
        context = super(BatchList, self).get_context_data(**kwargs)
        context['run_management_command'] = self.run_management_command(self.object.id)
        return context


class ItemListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Item
    queryset = Item.objects.order_by('id')
    context_object_name = 'item_list'
    table_class = ItemList
    template_name = 'item_list.html'
    paginate_by = 15
    context_object_name = 'item'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)

        # Session keys
        key = 'my_qs'
        key_url = 'key_url'

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        self.request.session[key] = b64encode(pickle.dumps(self.filterset.qs.query)).decode('ascii')

        self.request.session[key_url] = self.request.GET

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

    # Form
    def get_success_url(self):
        return reverse('itemupdateview', kwargs={'pk': self.object.pk})

    # Form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()

        if request.method == 'POST':
            if form.is_valid():
                if self.request.POST:
                    if 'save_add' in request.POST:
                        self.start_review_progress()
                        return self.form_valid(form)
                    elif 'save_continue' in request.POST:
                        self.form_valid(form)
                        self.start_review_progress()
                        pk_id = self.get_next_id(self.object.id)
                        return redirect('itemupdateview', pk=pk_id)
                    elif 'reset' in request.POST:
                        return HttpResponseRedirect(reverse('itemupdateview', kwargs={'pk': self.object.pk}))
            else:
                return self.form_invalid(form)

    # Form
    def form_valid(self, form):
        return super().form_valid(form)

    # Add info to the form
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        return kwargs

    # Update field when saved
    def start_review_progress(self, *args, **kwargs):
        if self.object.review_status == 0:
            self.object.review_status = 1
            self.object.save(update_fields=['review_status'])

    # Navigation
    def get_next_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = object_list.filter(id__gt=current_object_id).order_by('id').only('id').first()
        if qs:
            return qs.id
        else:
            return None

    # Navigation
    def get_previous_id(self, current_object_id, **kwargs):
        object_list = self.get_object_list()
        qs = object_list.filter(id__lt=current_object_id).order_by('-id').only('id').first()
        if qs:
            return qs.id
        else:
            return None

    # Get queryset from list view
    def get_object_list(self, **kwargs):
        # Session keys
        key = 'my_qs'

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        query = pickle.loads(b64decode(self.request.session[key]))
        qs = Item.objects.all()
        qs.query = query
        object_list = qs.order_by('id')
        return object_list

    # Create context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get query URL to return to list view
        key_url = 'key_url'
        query_params = self.request.session[key_url]

        context.update(
            {
                'query_params': urlencode(query_params),
                'current_object_id': self.object.id,
                'next_object_id': self.get_next_id(self.object.id),
                'previous_object_id': self.get_previous_id(self.object.id),
                'object_list': self.get_object_list(),
                'start_review_progress': self.start_review_progress(),
                'attachment_count': self.object.attachment_count,
                'inline_count': self.object.inline_count,
            }
        )

        try:  # If we have pk, then create item with that pk
            pk = self.kwargs['pk']
            instances = Item.objects.filter(pk=pk)
            if instances:
                kwargs['object'] = instances[0]
        except Exception:
            pass  # No pk, so no item
        return context
