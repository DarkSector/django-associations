__author__ = 'DarkSector'
from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from views import ShowAssociationsForApp, ShowInstalledApps, \
    ShowAllInstalledApps, ShowUsage, ShowAboutPage

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_ass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^installed/all$',
        ShowAllInstalledApps.as_view(),
        name='associations_installed_apps_all',
        ),

    url(r'^installed/$',
        ShowInstalledApps.as_view(),
        name='associations_installed_apps',
        ),

    url(r'^(?P<app_name>[ \w]+)/$',
        ShowAssociationsForApp.as_view(),
        name='associations_for_app',
    ),

    url(r'^usage/',
        ShowUsage.as_view(),
        name='app_usage',
        ),

    url(r'^about',
        ShowAboutPage.as_view(),
        name="show_about_page",
        ),

    url(r'^',
        RedirectView.as_view(url='/associations/installed/'),
        name='front_page',
        ),




)
