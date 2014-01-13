__author__ = 'DarkSector'
from django.conf.urls import patterns, url
from views import ShowAssociationsForApp, ShowInstalledApps, \
    ShowAllInstalledApps, ShowUsage

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_ass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^installed/all$',
        ShowAllInstalledApps.as_view(),
        name='ass_installed_apps_all'),

    url(r'^installed/$',
        ShowInstalledApps.as_view(),
        name='ass_installed_apps'),

    url(r'^(?P<app_name>[ \w]+)/$',
        ShowAssociationsForApp.as_view(),
        name='ass'),

    url(r'^',
        ShowUsage.as_view(),
        name='app_usage' ),


)
