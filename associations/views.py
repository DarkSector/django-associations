from django.shortcuts import render
import os
import sys
import imp
import importlib
from django.views.generic import TemplateView
from utils import get_all_apps_regex, get_non_django_apps_regex, \
    get_app_name_regex_from_app_urls

# Create your views here.
class ShowUsage(TemplateView):
    template_name = 'usage.html'

    def get_context_data(self, **kwargs):
        context = super(ShowUsage, self).get_context_data(**kwargs)
        context['usage'] = True
        return context


class ShowAboutPage(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(ShowAboutPage, self).get_context_data(*kwargs)
        context['about'] = True
        return context


class ShowAssociationsForApp(TemplateView):
    template_name = "associations.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ShowAssociationsForApp, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        app_name = self.kwargs.get('app_name')
        # get app_name and then get associations for it.

        associations_dict = get_app_name_regex_from_app_urls(app_name)


        context = super(ShowAssociationsForApp, self).get_context_data(**kwargs)
        context.update({
            'associations' : associations_dict,
            'app_name': app_name,
        })
        return context


class ShowInstalledApps(TemplateView):
    template_name = "list_apps.html"

    def dispatch(self, request, *args, **kwargs):
        return super(ShowInstalledApps, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        #_apps = get_installed_apps_names()
        apps = get_non_django_apps_regex()
        context = super(ShowInstalledApps, self).get_context_data(*args, **kwargs)
        context['installed_apps'] = apps
        context['installed_apps_flag'] = True
        return context


class ShowAllInstalledApps(TemplateView):
    template_name = "list_apps.html"

    def get_context_data(self, *args, **kwargs):
        apps = get_all_apps_regex()

        context = super(ShowAllInstalledApps, self).get_context_data(*args, **kwargs)
        context.update({
            'installed_apps': apps,
            'installed_apps_flag': True,
            'show_all': True,
        })
        return context