from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import FileResponse, HttpResponseForbidden, HttpResponseRedirect
from django.http.response import StreamingHttpResponse
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import TemplateView

import logging
import pickle

from base64 import b64encode, b64decode
import pandas as pd 
import plotly.express as px

from .filters import BatchFilter, ItemFilter
from .forms import BatchForm, ItemUpdateForm
from .models import Batch, Item
from processing.common.convert_and_export import convert_and_export


logger = logging.getLogger(__name__)

LIST_PAGINATE_BY = 20


class Index(TemplateView):
    template_name = 'index.html'


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'dashboard.html'
    model = Batch
    context_object_name = 'batch'

    def test_func(self):
        return self.request.user.is_staff
    
    def batch_chart(self):
        entries = Batch.objects.all()
        column_names = [field.name for field in Batch._meta.get_fields()]
    
        df = pd.DataFrame(columns = column_names)

        for element in entries:       
            new_entry = {"name":element.name, "Not Started":element.not_started_item_count , "In Progress":element.in_progress_total_item_count, "Complete":element.complete_total_item_count}
            df = df._append(new_entry, ignore_index=True)
        
        fig = px.bar(df, x='name', y=["Not Started", "In Progress", "Complete"], title='Review Status', text_auto=True, color_discrete_sequence=[ 'red','yellow','green'])
        fig.update_layout(xaxis = {'type' : 'category'}, xaxis_title="Batch Name", yaxis_title="Number of Items", legend_title="Review Status",)

        batch_chart = fig.to_html()
        return batch_chart   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                'batch_chart': self.batch_chart,
            }
        )
        return context


class BatchList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Batch
    context_object_name = 'batch_list'
    template_name = 'batch_list.html'
    paginate_by = LIST_PAGINATE_BY

    queryset = Batch.objects.all().order_by('id')

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return 'partials/batch_list_results.html'
        return self.template_name

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = BatchFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super(BatchList, self).get_context_data(**kwargs)

        context.update(
            {
                'form': self.filterset.form,
                'paginate_by': self.paginate_by,
            }
        )
        return context


def edit_batch(request, batch_pk):
    batch = Batch.objects.get(pk=batch_pk)
    context = {}
    context['batch'] = batch
    context['form'] = BatchForm(
        initial={
            'assigned_to': batch.assigned_to,
        }
    )
    return render(request, 'partials/edit_batch.html', context)


def edit_batch_submit(request, batch_pk):
    context = {}
    batch = Batch.objects.get(pk=batch_pk)
    context['batch'] = batch
    if request.method == 'POST':
        form = BatchForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'partials/edit_batch.html', context)
    return render(request, 'partials/batch_list_results_row_assigned_to.html', context)


class ItemListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Item
    context_object_name = 'item_list'
    template_name = 'item_list.html'
    paginate_by = LIST_PAGINATE_BY

    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return 'partials/item_list_results.html'
        return self.template_name

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = Item.objects.filter(batch=self.request.resolver_match.kwargs['batch']).order_by('id')
        self.filterset = ItemFilter(self.request.GET, queryset=queryset)

        # Session keys
        key = 'my_qs'
        key_url = 'key_url'

        # Django wants datatypes to be JSON serializable. Byte objects need to be encoded/decoded
        self.request.session[key] = b64encode(pickle.dumps(self.filterset.qs.query)).decode('ascii')

        self.request.session[key_url] = self.request.GET

        return self.filterset.qs

    def item_list_batch(self, **kwargs):
        item_list_batch = self.request.resolver_match.kwargs['batch']
        return item_list_batch
    
    def item_list_batch_name(self, **kwargs):
        batch_id = self.request.resolver_match.kwargs['batch']
        item_list_batch_name = Batch.objects.get(pk=batch_id).name
        return item_list_batch_name

    def total_item_count(self):
        items_set = Item.objects.filter(batch=self.request.resolver_match.kwargs['batch']).count()
        return items_set
    
    def not_started_item_count(self):
        items_set = Item.objects.filter(batch=self.request.resolver_match.kwargs['batch'], review_status=0).count()
        return items_set
    
    def in_progress_total_item_count(self):
        items_set = Item.objects.filter(batch=self.request.resolver_match.kwargs['batch'], review_status=1).count()
        return items_set
    
    def complete_total_item_count(self):
        items_set = Item.objects.filter(batch=self.request.resolver_match.kwargs['batch'], review_status=2).count()
        return items_set

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        item_filter = ItemFilter(self.request.GET, queryset=self.queryset)
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']

        context.update(
            {
                'query_params': query_params.urlencode(),
                'form': self.filterset.form,
                'items': item_filter.qs,
                'item_list_batch': self.item_list_batch,
                'paginate_by': self.paginate_by,
                'item_list_batch_name': self.item_list_batch_name,
                'total_item_count': self.total_item_count,
                'not_started_item_count': self.not_started_item_count,
                'in_progress_total_item_count': self.in_progress_total_item_count,
                'complete_total_item_count': self.complete_total_item_count,

            }
        )
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'item_view.html'
    model = Item
    form_class = ItemUpdateForm
    context_object_name = 'item'

    def test_func(self):
        return self.request.user.is_staff

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

    # Get applied filter(s) to return to list view
    def get_query_params_without_page(self):
        key_url = 'key_url'
        query_params_without_page = self.request.session[key_url].copy()

        try:
            del query_params_without_page['page']
        except KeyError:
            pass

        return query_params_without_page

    # Get list view page that current item would be located
    def get_current_list_page(self, current_object_id):
        page_size = LIST_PAGINATE_BY
        object_list = self.get_object_list()
        num_preceeding_results = object_list.filter(id__lt=current_object_id).count()
        current_list_page = num_preceeding_results // page_size + 1

        return current_list_page

    # Get query URL to return to list view
    def get_query_params(self, **kwargs):
        key_url = 'key_url'
        query_params = self.request.session[key_url]
        query_params = urlencode(query_params)
        return query_params

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

        context.update(
            {
                'query_params_without_page': urlencode(self.get_query_params_without_page()),
                'current_object_id': self.object.id,
                'next_object_id': self.get_next_id(self.object.id),
                'previous_object_id': self.get_previous_id(self.object.id),
                'object_list': self.get_object_list(),
                'start_review_progress': self.start_review_progress(),
                'attachment_count': self.object.attachment_count,
                'inline_count': self.object.inline_count,
                'external_count': self.object.external_count,
                'current_list_page': self.get_current_list_page(self.object.id),
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


class FinalizeBatchView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'finalize_batch.html'
    queryset = Batch.objects.all()

    def test_func(self):
        return self.request.user.is_staff

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


def batch_convert_and_export(request):
    batch_selected = request.POST['id']
    stream = convert_and_export(batch_selected)
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response


@login_required
def protected_media(request, directory, filename):
    if request.user.is_staff:
        response = FileResponse(open(settings.MEDIA_ROOT + '/' + directory + '/' + filename, 'rb'))
        return response


def error_400(request, exception):
    return render(request, '404.html', status=400)


def error_403(request, exception):
    return render(request, '404.html', status=403)


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    data = {}
    return render(request, '500.html', data)
