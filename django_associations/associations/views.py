# Create your views here.
from django.views.generic import TemplateView

from .api import get_association_list, parse_class_based_views


class AssociationsView(TemplateView):
    template_name = "basic.html"

    def get_context_data(self, **kwargs):
        context = super(AssociationsView, self).get_context_data(**kwargs)
        associations = get_association_list()
        # class_based_update_view_module = parse_class_based_views("testapp2.views.ClassBasedViews"
        #                                                          ".DoubleClassBasedTemplateViewNoAttributeOverride")
        context.update({
            "associations": associations
        })
        return context
