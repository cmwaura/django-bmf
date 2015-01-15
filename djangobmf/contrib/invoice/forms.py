#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.forms import ModelForm

from .models import Invoice


class InvoiceUpdateForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_number', ]


class InvoiceCreateForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_number', 'state', 'shipping_address', 'invoice_address', 'valid_until']
