__author__ = 'DarkSector'
import os
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
    """
    list_of_installed_apps = []
    list_of_python_installed_packages = []

    for distribution in pip.get_installed_distributions():
        # somehow it gives an error if it's not string later on
        list_of_python_installed_packages.append(str(distribution))

    django_settings = get_django_settings()
    installed_apps = django_settings.INSTALLED_APPS

    #print installed_apps
    for app in installed_apps:
        if not 'django' in app:
            # check if the name django doesn't come in
            for dist_name in list_of_python_installed_packages:
                # check if the name isn't in any individual app name
                # in the installed python packages
                if not app in dist_name:
                    # if not present
                    # allow the url to be parsed
                    list_of_installed_apps.append(app)
    return list_of_installed_apps