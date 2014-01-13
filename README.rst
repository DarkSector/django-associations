=====
Associations
=====

Associations is a simple Django app to show associations between urls and templates of an app. For each app a list of views, view names, view types and urls are shown

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "associations" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'associations',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^associations/', include('associations.urls')),

3. Start the development server and visit http://127.0.0.1:8000/associations/ and you're done