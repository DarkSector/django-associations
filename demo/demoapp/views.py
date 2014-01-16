from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from models import Demo
from forms import DemoForm


# Create your views here.
class CreateDemoPageView(CreateView):
    template_name = 'create_demo.html'
    model = Demo
    form_class = DemoForm

    def get_success_url(self):
        return reverse('list_demo')


class ListDemoPageView(ListView):
    template_name = 'list_demo.html'
    model = Demo

class DetailDemoView(DetailView):
    template_name = 'detail_demo.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Demo, pk=self.kwargs.get('pk'))
        return obj

# class FooView(View):
#     def dispatch(self, request, *args, **kwargs):
#         return super(FooView, self).dispatch(request, *args, **kwargs)

class FooView(TemplateView):
    template_name = 'list_demo.html'
