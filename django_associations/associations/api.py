from typing import List, Tuple, Dict

from django.conf import settings
from django.urls import URLResolver
from django_extensions.management.commands.show_urls import (URLPattern, describe_pattern,
                                                             ViewDoesNotExist)
import inspect


def extract_views_from_urlpatterns(urlpatterns, base='', namespace=None) -> List[Dict]:
    """
    Return a list of views from a list of urlpatterns.

    Each object in the returned list is a three-tuple: (view_func, regex, name)
    """
    views = []
    for p in urlpatterns:
        if isinstance(p, (URLPattern,)):
            try:
                if not p.name:
                    name = p.name
                elif namespace:
                    name = '{0}:{1}'.format(namespace, p.name)
                else:
                    name = p.name
                pattern = describe_pattern(p)
                try:
                    lookup_str = p.lookup_str
                except Exception:
                    lookup_str = None

                _data = {
                    "view_str": lookup_str,
                    "callback": p.callback,
                    "pattern": base + pattern,
                    "name": name
                }
                views.append(_data)
            except ViewDoesNotExist:
                continue
        elif isinstance(p, (URLResolver,)):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            if namespace and p.namespace:
                _namespace = '{0}:{1}'.format(namespace, p.namespace)
            else:
                _namespace = (p.namespace or namespace)
            pattern = describe_pattern(p)
            views.extend(extract_views_from_urlpatterns(patterns, base + pattern, namespace=_namespace))
        elif hasattr(p, '_get_callback'):
            try:
                views.append((p._get_callback(), base + describe_pattern(p), p.name))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + describe_pattern(p), namespace=namespace))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return views


def get_association_list():
    urlconf = __import__(getattr(settings, "ROOT_URLCONF"), {}, {}, [''])
    return extract_views_from_urlpatterns(urlconf.urlpatterns)


def parse_class_based_views(cbv_path: str, ignore_class: bool = True, ignore_functions: bool = True,
                            ignore_methods: bool = True) -> List[Tuple]:
    module_hierarchy = cbv_path.split(".")
    mod = __import__(module_hierarchy[0])
    for module in module_hierarchy[1:]:
        mod = getattr(mod, module)

    boring = dir(type('dummy', (object,), {}))

    final = []
    for item in inspect.getmembers(mod):
        if item[0] not in boring:

            if ignore_class:
                if inspect.isclass(item[1]):
                    continue
            if ignore_functions:
                if inspect.isfunction(item[1]):
                    continue
            if ignore_methods:
                if inspect.ismethod(item[1]):
                    continue

            final.append(item)

    return final
