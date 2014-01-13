__author__ = 'DarkSector'
import os
import sys
import imp
import importlib
import inspect
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist


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
    """
    django_settings = get_django_settings()
    root_urls_from_settings = django_settings.ROOT_URLCONF
    base_dir = get_base_dir_path()
    root_urls_path = root_urls_from_settings.replace('.','/')
    root_urls_abspath = base_dir + '/' + str(root_urls_path) + '.py'
    root_urls_module = imp.load_source(root_urls_from_settings.split('.')[1],root_urls_abspath)
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
    django_settings = get_django_settings()
    installed_apps = django_settings.INSTALLED_APPS
    for app in installed_apps:
        if not 'django' in app:
            list_of_installed_apps.append(app)
    return list_of_installed_apps


def get_pattern_package_name(pattern):
    """
    Returns the package name of the url pattern being analyzed
    """
    app_name = None
    if hasattr(pattern, 'app_name'):
        app_name = pattern.app_name
        if not app_name:
            app_name = pattern.urlconf_name.__package__
    return app_name


def is_admin_package(url_pattern):
    """
    Return True or False
    If the url_pattern being analyzed belongs to Admin package
    """
    if hasattr(url_pattern, 'app_name'):
        # if 'app_name' exists
        # check if that app_name is admin
        if url_pattern.app_name == 'admin':
            return True
    return False


def admin_app_is_installed():
    """
    Return Boolean after checking if
    django.contrib.admin is installed
    """
    all_installed_apps = get_all_installed_apps_names()
    for app in all_installed_apps:
        if app == 'django.contrib.admin':
            return True
    return False


def is_in_installed_apps(url_pattern):
    """
    Checks to see if the pattern is relevant
    It checks against INSTALLED_APPS in Django Settings
    If package is admin and it exists in installed_apps
    Return True
    """
    installed_apps = get_all_installed_apps_names()
    pattern_package_name = get_pattern_package_name(url_pattern)
    if is_admin_package(url_pattern) and admin_app_is_installed():
        return True
    elif pattern_package_name in installed_apps:
            return True
    return False


def get_admin_url_pattern():
    if admin_app_is_installed():
        for url_pattern in get_root_urls().urlpatterns:
            if get_pattern_package_name(url_pattern) == 'admin':
                return url_pattern
    return None

def get_non_django_installed_url_patterns():
    """
    Get all the non django urlpatterns
    defined in base urls.py
    """
    allowed_urls = []
    root_urls = get_root_urls()
    installed_apps = get_non_django_installed_apps()
    for url_pattern in root_urls.urlpatterns:
        pkg_name = get_pattern_package_name(url_pattern)
        if pkg_name in installed_apps:
            allowed_urls.append(url_pattern)
    return allowed_urls


def get_all_installed_url_patterns():
    """
    Returns a list of urlpatterns that
    are defined in base urls.py
    """
    allowed_urls = []
    root_urls = get_root_urls()
    for url_pattern in root_urls.urlpatterns:
        if is_in_installed_apps(url_pattern):
            allowed_urls.append(url_pattern)
    return allowed_urls


def get_non_django_apps_regex():
    """
    Returns dict of non django app names installed
    and specified in the base urls.py
    """
    apps_and_regex = {}
    url_patterns = get_non_django_installed_url_patterns()
    for url_pattern in url_patterns:
        pkg_name = get_pattern_package_name(url_pattern)
        apps_and_regex[pkg_name] = url_pattern._regex
    return apps_and_regex


def get_all_apps_regex():
    """
    Returns dict of app names and corresponding
    Regex expression from base urls.py
    Also returns the app names in INSTALLED APPS
    but not specified in the base urls.py
    """
    apps_and_regex = {}
    url_patterns = get_all_installed_url_patterns()
    for url_pattern in url_patterns:
        pkg_name = get_pattern_package_name(url_pattern)
        apps_and_regex[pkg_name] = url_pattern._regex
    for app_name in get_all_installed_apps_names():
        if app_name not in apps_and_regex.keys():
            apps_and_regex[app_name] = None
    return apps_and_regex


def get_base_url_pattern_by_app(app_name):
    root_urls = get_root_urls()
    for url_pattern in root_urls.urlpatterns:
        pkg_name = get_pattern_package_name(url_pattern)
        if pkg_name == app_name:
            return url_pattern
        elif app_name == 'admin':
            return get_admin_url_pattern()
    return None


# def get_app_name_regex(app_name):
#     """
#     {
#         'url_name': {
#                         'view_name': 'name of the view',
#                         'view_type': 'Type of view',
#                         'regex': '',
#                         'kwargs': 'the kwargs in the regex',
#                         'templates' : 'name of the template'
#                     }
#     }
#     """
#     views_and_regex = {}
#     app_url_pattern = get_base_url_pattern_by_app(app_name)
#     reverse_dict = app_url_pattern.reverse_dict
#     internal_dict = {}
#     for key in reverse_dict:
#         if hasattr(key, '__call__'):
#             # it's a function
#             internal_dict['view_name'] = key.func_name
#             views_module_string = key.__module__
#             # app_name = views_module_string.split('.')[0]
#             views_module = importlib.import_module(views_module_string)
#             key_class = getattr(views_module, str(key.func_name))
#             internal_dict['view_type'] = inspect.getmro(key_class)[1].__name__
#             key_class_instance = key_class()
#             internal_dict['templates'] = key_class_instance.get_template_names()
#     return views_and_regex


def get_app_patterns_from_app_urls(app_name):
    app_url_base_pattern = get_base_url_pattern_by_app(app_name)

    try:
        app_urls_module_name = app_url_base_pattern.urlconf_name.__name__
    except AttributeError:
        raise ObjectDoesNotExist("App name does not exist")
    app_urls_module = importlib.import_module(app_urls_module_name)
    return app_urls_module.urlpatterns


def get_app_name_regex_from_app_urls(app_name):

    views_and_regex = {}

    app_url_patterns = get_app_patterns_from_app_urls(app_name)


    for url_pattern in app_url_patterns:
        views_and_regex[url_pattern.name] = {}

        views_and_regex[url_pattern.name]['view_name'] = url_pattern._callback.func_name

        views_module_string = url_pattern._callback.__module__


        views_module = importlib.import_module(views_module_string)

        view_class = getattr(views_module, str(url_pattern._callback.func_name))

        class_instance = view_class()

        try:
            templates = class_instance.template_name
        except ImproperlyConfigured:
            templates = None
        views_and_regex[url_pattern.name]['templates'] = templates
        views_and_regex[url_pattern.name]['regex'] = url_pattern._regex

    return views_and_regex


def get_app_name_regex_from_app_urls_detailed(app_name):
    views_and_regex = {}
    app_url_patterns = get_app_patterns_from_app_urls(app_name)


    for url_pattern in app_url_patterns:
        views_and_regex[url_pattern.name] = {}

        views_and_regex[url_pattern.name]['view_name'] = url_pattern._callback.func_name

        views_module_string = url_pattern._callback.__module__
        views_module = importlib.import_module(views_module_string)
        view_class = getattr(views_module, str(url_pattern._callback.func_name))

        class_instance = view_class()

        try:
            templates = class_instance.template_name
        except ImproperlyConfigured:
            templates = None
        views_and_regex[url_pattern.name]['templates'] = templates
        views_and_regex[url_pattern.name]['regex'] = url_pattern._regex

    return views_and_regex
