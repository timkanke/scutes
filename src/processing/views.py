from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin, SingleTableView

import logging
import os
import pickle

from base64 import b64encode, b64decode

from .filters import ItemFilter
from .forms import ItemUpdateForm
from .models import Batch, Item
from .tables import BatchList
from processing.common.export import export
from processing.common.finalize_redactions import convert_redaction


logger = logging.getLogger(__name__)


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


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    queryset = Item.objects.order_by('id')
    context_object_name = 'item_list'
    template_name = 'item_list.html'
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
        item_filter = ItemFilter(self.request.GET, queryset=Item.objects.order_by('id'))

        context['form'] = self.filterset.form
        context['items'] = item_filter.qs
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


class FinalizeBatchView(LoginRequiredMixin, DetailView):
    template_name = 'finalize_batch.html'
    queryset = Batch.objects.all()

    def item_review_not_complete(self, **kwargs):
        batch_id = self.object.id
        qs = Item.objects.filter(batch=batch_id, review_status=1) | Item.objects.filter(batch=batch_id, review_status=0)
        if qs:
            return qs.count
        else:
            return None

    def item_publish(self):
        batch_id = self.object.id
        qs = Item.objects.filter(batch=batch_id, publish=1)
        return qs.count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'batch_id': self.object.id,
                'item_review_not_complete': self.item_review_not_complete(),
                'item_publish': self.item_publish(),
            }
        )
        return context


def batch_redaction(request):
    batch_selected = request.POST['id']
    stream = convert_redaction(batch_selected)
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def batch_export(request):
    batch_selected = request.POST['id']
    export_path = os.path.join(settings.MEDIA_ROOT, 'export')
    stream = export(batch_selected, export_path)
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
