.. _Emencia: http://www.emencia.com
.. _djangorestframework: http://www.django-rest-framework.org
.. _Gestus-client: https://github.com/sveetch/Gestus-client
.. _buildout: http://www.buildout.org/

**Gestus** is a Django app to collect and store datas about our Website projects at `Emencia`_.

Although there is the Django admin to manage the Gestus objects, there is also a REST part which is used to create and update Website datas with a client.

Introduction
============

Gestus will store some datas about your project :

* Its name and a description;
* Its kind of environnement (``integration`` or ``production``);
* Its server hostname;
* The URL where the website project is published;
* A list of installed packages with their version;

**There is actually no real frontend, development has been focused on the rest API but it is browsable.**

Require
*******

* `djangorestframework`_ >= 2.3

Install
=======

Add *PO Projects* to your installed apps in settings : ::

    INSTALLED_APPS = (
        ...
        'gestus'
        'rest_framework'
        ...
    )
    
Then add the `djangorestframework`_ settings : ::

    REST_FRAMEWORK = {
        'PAGINATE_BY': 10,
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS': (
            'rest_framework.serializers.HyperlinkedModelSerializer',
        ),

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAdminUser',
            #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        ),
    }

Finally mount its urls in your main ``urls.py`` : ::

    urlpatterns = patterns('',
        ...
        (r'^gestus/', include('gestus.urls', namespace='gestus')),
        (r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ...
    )

External API access
===================

With `djangorestframework`_ a rest API will be available on : ::

    /gestus/rest/

It is browsable for authenticated users with admin rights (``is_staff`` on True), also the client will need to access to the API with an user accounts with the admin rights.

`Gestus-client`_ is client to use the API from your project.
