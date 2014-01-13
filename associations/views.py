from django.shortcuts import render
import os
import sys
import imp
import importlib
from django.views.generic import TemplateView
from utils import get_all_apps_regex, get_non_django_apps_regex, \
    get_app_name_regex_from_app_urls

# Create your views here.
class ShowAppsView(TemplateView):

    template_name = 'list_apps.html'

    def get_primary_urls_module(self):
        self.base_dir = sys.path[0]
        urls_dir = sys.path[0] + '/django_ass/urls.py'
        urls = imp.load_source('django_ass.django_ass.urls', urls_dir)

        return urls

    def check_if_admin(self, url_to_check):
        if hasattr(url_to_check, 'app_name'):
            if url_to_check.app_name == 'admin':
                return True
        return False

    def get_view(self, pkgname, viewname):
        base_dir = self.base_dir
        # get the view name from the application
        pkgurl = base_dir + '/django_ass/'+ pkgname


    def get_base_urls(self):
        # get the urls in the main app
        self.list_of_base_urls = []

        # grab the primary module
        urls = self.get_primary_urls_module()


        self.list_of_apps = []

        for url in urls.urlpatterns:
            if not self.check_if_admin(url):
                # proceed with
                # creating a dict

                # {
                #     'app_name' : 'name of the application',
                #     {
                #         'view_name' : {'url' : 'template_name'},
                #         'view_name' : {'url' : 'template_name'},
                #
                #     }
                # }


                _app_name = url.urlconf_name.__package__


                _views = {}
                for key in url.reverse_dict:
                    # check if it's not a function
                    if hasattr(key, '__call__'):
                        # it's a function
                        # view name : the pattern
                        _views[key.func_name] = url.reverse_dict[key][0][0]

                _templates = {}
                # for key in _views:
                #     # for every view
                #     # import view from the app
                #     #

                for _view in _views:
                    get_view = importlib.import_module(_view)
                    class_instance = get_view()

                    if hasattr(class_instance, 'template_name'):
                        _templates[get_view] = class_instance.template_name
                    else:
                        pass

                        # app_name : <actual app name>
                _app = { 'app_name' : _app_name,
                         # views : contains the views formed above
                         'views' : _views,
                         # templates : view name
                         'templates' : _templates,
                    }

                self.list_of_apps.append(_app)
        return self.list_of_apps


    def get_context_data(self, **kwargs):
        context = super(ShowAppsView, self).get_context_data(**kwargs)
        context['urls'] = self.get_base_urls()
        return context


class ShowUsage(TemplateView):
    template_name = 'usage.html'

    def get_context_data(self, **kwargs):
        context = super(ShowUsage, self).get_context_data(**kwargs)
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