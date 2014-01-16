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

    New in 0.1.6: Doesn't consider the apps installed using pip
    """
    list_of_installed_apps = []

    django_settings = get_django_settings()
    installed_apps = django_settings.INSTALLED_APPS

    #print installed_apps
    for app in installed_apps:
        if not app_name_has_django_in_it(app):# and not app_matches_with_installed_python_packages(app):
            list_of_installed_apps.append(app)
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


def app_matches_with_installed_python_packages(app_name):
    """
    Return True if app_name matches any package name in
    the list of installed distributions returned
    by pip.get_installed_distributions()
    """
    list_of_python_installed_packages = [str(pkg) for pkg in pip.get_installed_distributions()]
    for pkg in list_of_python_installed_packages:
        rel = pkg
        # rg = re.compile(rel, re.IGNORECASE|re.DOTALL)
        m = pkg.search(app_name)
        if m:
            return True
    return False