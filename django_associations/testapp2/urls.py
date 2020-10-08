from django.urls import path
from .views import ModularizedClassBasedTemplateView, InheritedClassBasedTemplateView, DoubleClassBasedTemplateViewNoAttributeOverride

urlpatterns = [
    path('mod_template/', ModularizedClassBasedTemplateView.as_view(), name='modularized_cbv_template_view'),
    path('mod_inherited/', InheritedClassBasedTemplateView.as_view(), name='inherited_cbv_template_view'),
    path('mod_double_inherited/', DoubleClassBasedTemplateViewNoAttributeOverride.as_view(random_keyword=True), name='double_inherited_cbv_template_view')
]
