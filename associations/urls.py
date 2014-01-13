__author__ = 'DarkSector'
from django.conf.urls import patterns, url
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

    url(r'^about',
        ShowAboutPage.as_view(),
        name="show_about_page",
        ),

    url(r'^',
        ShowUsage.as_view(),
        name='app_usage',
        ),


)
