#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from djangobmf.views import ModuleListView
from djangobmf.views import ModuleCreateView
from djangobmf.views import ModuleUpdateView
from djangobmf.views import ModuleDetailView

from .forms import InvoiceUpdateForm
from .forms import InvoiceCreateForm


class AllInvoiceView(ModuleListView):
    name = _("All Invoices")
    slug = "all"
    date_resolution = "month"


class OpenInvoiceView(ModuleListView):
    name = _("Open Invoices")
    slug = "open"


class InvoiceCreateView(ModuleCreateView):
    form_class = InvoiceCreateForm


class InvoiceUpdateView(ModuleUpdateView):
    form_class = InvoiceUpdateForm


class InvoiceDetailView(ModuleDetailView):
    pass
