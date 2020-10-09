from django.urls import path
from django.views.generic import TemplateView

from .views import ClassBasedCreateView, ClassBasedFormView, ClassBasedDeleteView, ClassBasedTemplateView, \
    ClassBasedListView, ClassBasedUpdateView

urlpatterns = [
    path('list/', ClassBasedListView.as_view(), name='cbv_list'),
    path('create/', ClassBasedCreateView.as_view(), name='cbv_create'),
    path('form/', ClassBasedFormView.as_view(), name='cbv_form'),
    path('delete/', ClassBasedDeleteView.as_view(), name='cbv_delete'),
    path('template/', ClassBasedTemplateView.as_view(), name='cbv_template'),
    path('update/', ClassBasedUpdateView.as_view(), name='cbv_update'),
    path('inline_generic_view/', TemplateView.as_view(template_name="my_template.html"), name='cbv_inline_template'),
]
