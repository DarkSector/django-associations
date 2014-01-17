__author__ = 'DarkSector'
import os
import re
import sys
import pip
import imp
import importlib

def get_django_settings():
    """
    Returns the Django Settings Package/Module.
    Not the path
    """
    django_settings_module_name = os.environ['DJANGO_SETTINGS_MODULE']
    django_python_path = sys.path[0]
    django_settings_module = imp.load_source(django_settings_module_name, django_python_path)
    return django_settings_module


def get_base_dir_path():
    """
    Returns the BASE_DIR path located in Django Settings package
    """
    django_settings = get_django_settings()
    base_dir_path = django_settings.BASE_DIR
    python_path = sys.path[0]
    return base_dir_path


def get_root_urls():
    """
    Returns the Base URLS module.
    Base urls.py
    Also known as ROOT_URLCONF
    """
    django_settings = get_django_settings()
    root_urls_from_settings = django_settings.ROOT_URLCONF
    base_dir = get_base_dir_path()
    root_urls_module = importlib.import_module(root_urls_from_settings, base_dir)
    return root_urls_module


def get_project_name():
    """
    Returns the name of the project
    """
    django_settings_path = os.environ['DJANGO_SETTINGS_MODULE']
    base_dir_name = django_settings_path.split('.')[0]
    return base_dir_name


def get_all_installed_apps_names():
    """
    Gets a list of Django Installed Apps Names/strings
    """
    django_settings = get_django_settings()
    installed_apps = django_settings.INSTALLED_APPS
    return list(installed_apps)


def get_non_django_installed_apps():
    """
    Returns a list of all the non django apps installed

    New in 0.1.6: Doesn't consider apps that haven't been created
    by the user
    """
    list_of_installed_apps = []

    django_settings = get_django_settings()
    installed_apps = django_settings.INSTALLED_APPS

    for app in installed_apps:
        if not app_name_has_django_in_it(app):
            # filter out all apps that are not created by user
            # first get their base package name
            base_pkg_name = get_installed_app_main_package_name(app)
            # then check if that particular base package is in os.path
            if is_user_made_app(base_pkg_name):
                # if os.path.exists() is true
                list_of_installed_apps.append(app)
            # this takes care of apps that are a part of Django
            # If you create an app called django.foo.something
            # you're generating a conflict, therefore your app
            # won't be called django.something unless you're
            # stupid.
    return list_of_installed_apps


def app_name_has_django_in_it(app_name):
    """
    Return True if app_name contains the word django
    """
    rel = '(django)'
    rg = re.compile(rel, re.IGNORECASE|re.DOTALL)
    m = rg.search(app_name)
    if m:
        return True
    return False


def get_installed_app_main_package_name(app_name):
    """
    For apps like
    cms.foo.bar
    you get their base package name 'cms'
    """
    return app_name.split('.')[0]


def is_user_made_app(app_name):
    """
    This is an interesting way
    Simply check if os.path.exists() is True
    """
    base_url = get_base_dir_path()
    app_full_path = base_url + '/' + app_name
    return os.path.exists(app_full_path)
