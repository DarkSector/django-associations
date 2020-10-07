# Create your views here.
from django.views.generic import TemplateView

from .api import get_association_list


class AssociationsView(TemplateView):
    template_name = "basic.html"

    def get_context_data(self, **kwargs):
        context = super(AssociationsView, self).get_context_data(**kwargs)
        context.update({
            "associations": get_association_list()
        })
        return context
