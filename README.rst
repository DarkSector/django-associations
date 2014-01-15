============
Associations
============

Associations is a simple Django app to show associations between urls and other attributes in the installed applications.
For each app a list of views, view names, view types and urls are shown. When debugging an app, the common and the most
straightforward way is to trace the view or template through urls.py of the app. Associations places all of these
template names and view names on a single page so that you don't need to go through the process of locating the
template/view through the urls.

Requirements
============

Currently works with Django 1.5 above and Python 2.7.x.
Currently the docs and tests are being written and aren't complete


Quick start
===========

1. Add "associations" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'associations',
    )


2. Include the BASE_DIR in your project settings like this::

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


   If the 'BASE_DIR' is defined as some other variable, define BASE_DIR = <variable name>


2. Include the Associations URLconf in your project urls.py like this::

    url(r'^associations/', include('associations.urls')),


3. Start the development server and visit http://127.0.0.1:8000/associations/ and you're ready to go.