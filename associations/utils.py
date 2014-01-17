__author__ = 'DarkSector'

import importlib
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from bootstraputils import get_root_urls, get_django_settings, \
    get_base_dir_path, get_project_name, get_all_installed_apps_names, \
    get_non_django_installed_apps


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
        elif url_pattern is None:
            url_pattern_app_name = get_pattern_package_name(url_pattern)
            if url_pattern_app_name == 'django.contrib.admindocs':
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
    """
    Given the app_name to the method, it searches for
    the package name it belongs too. Once the package name
    is retrieved the corresponding REGEXURLResolver instance
    is returned. That is essentially the URL Pattern

    This particular method doesn't allow Admin app for now
    """
    root_urls = get_root_urls()
    for url_pattern in root_urls.urlpatterns:
        pkg_name = get_pattern_package_name(url_pattern)
        if pkg_name == app_name:
            return url_pattern
        elif app_name == 'admin':
            return get_admin_url_pattern()
    return None


def get_app_patterns_from_app_urls(app_name):
    """
    App name is given to the method and
    it retrieves the corresponding url patterns
    from the app module

    If the app name doesn't exist, It raises an exception
    """
    app_url_base_pattern = get_base_url_pattern_by_app(app_name)
    try:
        app_urls_module_name = app_url_base_pattern.urlconf_name.__name__
    except AttributeError:
        raise ObjectDoesNotExist("App name does not exist")
    app_urls_module = importlib.import_module(app_urls_module_name)
    return app_urls_module.urlpatterns


def get_app_name_regex_from_app_urls(app_name):
    """
    Returns a dict of url_name and view name and template name
    However the template_name may not be specified for a CBV

    Therefore a method needs to be written to retrieve template names
    by looking at model name and the kind of view.

    Specified here
    https://docs.djangoproject.com/en/1.5/topics/class-based-views/generic-display/

    For the intended change django.template.loaders.app_directories.Loader
    must be installed in the TEMPLATE_LOADERS

    """
    views_and_regex = {}
    app_url_patterns = get_app_patterns_from_app_urls(app_name)
    for url_pattern in app_url_patterns:
        views_and_regex[url_pattern.name] = {}
        views_and_regex[url_pattern.name]['view_name'] = url_pattern._callback.func_name
        views_module_string = url_pattern._callback.__module__
        views_module = importlib.import_module(views_module_string)
        view_class = getattr(views_module, str(url_pattern._callback.func_name))
        class_instance = view_class()
        if hasattr(class_instance, 'template_name'):
            templates = class_instance.template_name
        else:
            templates = None
        views_and_regex[url_pattern.name]['templates'] = templates
        views_and_regex[url_pattern.name]['regex'] = url_pattern._regex
    return views_and_regex