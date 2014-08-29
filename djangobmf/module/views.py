#!/usr/bin/python
# ex:set fileencoding=utf-8:

from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.views.generic.base import TemplateView

from ..viewmixins import ViewMixin


class ModuleView(ViewMixin, TemplateView):
    template_name = "djangobmf/modules.html"

    def get_context_data(self, **kwargs):
        from ..sites import site

        modules = []
        for ct, model in site.models.items():
            info = model._meta.app_label, model._meta.model_name
            perm = '%s.view_%s' % info
            if self.request.user.has_perms([perm, ]):
                key = force_text(model._bmfmeta.category)
                modules.append({
                    'category': key,
                    'model': model,
                    'name': model._meta.verbose_name_plural,
                    'url': model._bmfmeta.url_namespace + ':index',
                })

        context = super(ModuleView, self).get_context_data(**kwargs)
        context['modules'] = modules
        return context