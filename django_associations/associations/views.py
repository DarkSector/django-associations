from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView
from .api import get_association_list


class AssociationsView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(content=get_association_list())
