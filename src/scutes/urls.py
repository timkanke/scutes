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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


from processing.views import (
    About,
    BatchList,
    batch_convert_and_export,
    Dashboard,
    edit_batch,
    edit_batch_submit,
    FinalizeBatchView,
    Index,
    ItemListView,
    ItemUpdateView,
    protected_media,
)


# Custom 400, 403, 404, and 500 pages
handler400 = 'processing.views.error_400'
handler403 = 'processing.views.error_403'
handler404 = 'processing.views.error_404'
handler500 = 'processing.views.error_500'


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('about/', About.as_view(), name='about'),
    path('batchlist/', BatchList.as_view(), name='batchlist'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('', Index.as_view(), name='index'),
    path('itemlist/<int:batch>/', ItemListView.as_view(), name='itemlistview'),
    path('finalizebatch/<int:pk>/', FinalizeBatchView.as_view(), name='finalizebatchview'),
    path('batch_convert_and_export/', batch_convert_and_export, name='batch_convert_and_export'),
    path('itemview/<int:pk>/', ItemUpdateView.as_view(), name='itemupdateview'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('media/<str:directory>/<str:filename>', protected_media),
    re_path(r'saml2/', include('djangosaml2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

htmx_urlpatterns = [
    path('<int:batch_pk>/edit_batch/', edit_batch, name='edit_batch'),
    path('<int:batch_pk>/edit_batch_submit/', edit_batch_submit, name='edit_batch_submit'),
]

urlpatterns += htmx_urlpatterns


def get_navigation_links(request: HttpRequest):
    if request.user.is_authenticated:
        authenticated_links = {
            'dashboard': 'Dashboard',
            'batchlist': 'Batch List',
            '': f'Logged in as {request.user.username}',
            'saml2_logout': 'Log Out',
        }
        if request.user.is_superuser:
            superuser_links = {
                'admin:index': 'Admin',
            }
        else:
            superuser_links = {}
        links = {**superuser_links, **authenticated_links}
        return links
    else:
        return {'saml2_login': 'Log In'}
    

def get_footer_links(request: HttpRequest):
    if request.user.is_authenticated:
        authenticated_links = {
            'about': 'About',
        }
        if request.user.is_superuser:
            superuser_links = {
            }
        else:
            superuser_links = {}
        links = {**superuser_links, **authenticated_links}
        return links
    else:
        return {'saml2_login': 'Log In'}
