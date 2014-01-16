============
Associations
============


What is Associations?
=====================


Associations is a small app created to help Django developers.


What does it do?
================


It lists urls in an app along with the names of templates, views and urls associated with it

.. image:: https://raw.github.com/DarkSector/django-associations/master/associations/static/images/associations1.png
.. image:: https://raw.github.com/DarkSector/django-associations/master/associations/static/images/associations2.png


Why was it created?
===================


When working on a View, the common method of debugging or back tracing an issue is usually this:
 1. Look at the URL in the browser's address bar
 2. Decipher the app name from the URL
 3. Open the app project tree in your IDE (if not already open)
 4. Open the app's urls.py and locate the URL
 5. Look for the corresponding view
 6. Locate the view
 7. Locate the template name and subsequently the template itself.

 *Associations* on the other hand lists all of them on a single page, thereby decreasing the
 some times frustrating trace back.


Great, but what's the catch?
============================


The catch is that right now it's shown to be compatible with Class Based Views. It may or may not
work with traditional Function Based Views. Furthermore it has been tested on Django 1.5+ and Python 2.7.x.
There are plans to support Python 3 and Django 1.3+ in the near future.


Like to help out?
=================


You can find the Github repository here::

    https://github.com/DarkSector/django-associations

Log issues or start developing. The documentation is currently being written.


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