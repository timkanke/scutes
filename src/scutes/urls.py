"""
URL configuration for scutes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from processing.views import (
    BatchList,
    batch_export,
    batch_redaction,
    Dashboard,
    FinalizeBatchView,
    Index,
    ItemListView,
    ItemUpdateView,
)

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('batchlist/', BatchList.as_view(), name='batchlist'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('', Index.as_view(), name='index'),
    path('itemlist/<int:batch>/', ItemListView.as_view(), name='itemlistview'),
    path('finalizebatch/<int:pk>/', FinalizeBatchView.as_view(), name='finalizebatchview'),
    path('batch_redaction/', batch_redaction, name='batch_redaction'),
    path('batch_export/', batch_export, name='batch_export'),
    path('itemview/<int:pk>/', ItemUpdateView.as_view(), name='itemupdateview'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'password_reset//',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_reset_form.html', success_url='/'),
        name='change_password',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
