from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView, ListView

from .forms import MyForm
from .models import MyModel


class ClassBasedTemplateView(TemplateView):
    template_name = "my_template.html"


class ClassBasedFormView(FormView):
    form_class = MyForm
    template_name = "my_template.html"


class ClassBasedCreateView(CreateView):
    model = MyModel
    template_name = "my_template.html"


class ClassBasedUpdateView(UpdateView):
    model = MyModel
    template_name = "my_template.html"


class ClassBasedDeleteView(DeleteView):
    model = MyModel
    template_name = "my_template.html"


class ClassBasedListView(ListView):
    model = MyModel
    template_name = "my_template.html"
