from django.views.generic import TemplateView


class ModularizedClassBasedTemplateView(TemplateView):
    template_name = "another_template.html"


class InheritedClassBasedTemplateView(ModularizedClassBasedTemplateView):
    template_name = "second_template.html"
    random_keyword = False


class DoubleClassBasedTemplateViewNoAttributeOverride(InheritedClassBasedTemplateView):
    pass