.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/medialog.newsletter/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/medialog.newsletter/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/medialog.newsletter/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/medialog.newsletter?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/medialog.newsletter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/medialog.newsletter

.. image:: https://img.shields.io/pypi/v/medialog.newsletter.svg
    :target: https://pypi.python.org/pypi/medialog.newsletter/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/medialog.newsletter.svg
    :target: https://pypi.python.org/pypi/medialog.newsletter
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/medialog.newsletter.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/medialog.newsletter.svg
    :target: https://pypi.python.org/pypi/medialog.newsletter/
    :alt: License


===================
medialog.newsletter
===================

Send Newsletters from Plone.


Features
--------

- Adds a Content Type: Newsletter
- Newsletter has Title, Description and BodyText
- Newsletter has setting 'Items to send' (default=4)
- Newsletter has (button): Send testmail (sends to current user)
- Newsletter has (buttons): Send to everybody
- There are two views
  - @@manage-subscribers: (admin) view to see all subscribers and add / remove user   
  - @subscribe: view to subscribe / unsubscribe 


 

Documentation
-------------

Full documentation for end users can be found in the "docs" folder, and is also available online at http://docs.plone.org/foo/bar


Translations
------------

This product has been translated into

- Dutch (partly)


Installation
------------

Install medialog.newsletter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        medialog.newsletter


and then running ``bin/buildout``


Authors
-------

Provided by awesome people ;)


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/medialog.newsletter/issues
- Source Code: https://github.com/collective/medialog.newsletter
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
