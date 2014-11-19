Online Labs API Python Wrapper
================================

Heavily Inspired by [dopy](https://github.com/devo-ps/dopy).

Installation
============

.. code-block:: bash
    
    # pip install git+https://github.com/adebarbara/olpy

Getting Started
===============

To interact with Online Labs, you first need .. a online labs account.

.. code-block:: pycon

    >>> from olpy.manager import OlManager
    >>> ol = OlManager('api_token')

Or if you don't have a token

.. code-block:: pycon

    >>> from olpy.manager import OlManager
    >>> ol = OlManager()
    >>> token = ol.new_token('email','password')['id']
    >>> ol.set_token(token)


Methods
=======

The methods of the OlManager are self explanatory; ex.

.. code-block:: pycon

    >>> ol.servers()
    >>> ol.server('server_id')
    >>> ol.new_server('name', 'organization_id', 'image_id', ['volume_id'], ['tag'])
    >>> ol.delete_server('server_id')
    >>> ol.images()
    >>> ol.new_image('name', 'organization_id', 'image_id', 'arch', 'volume_id')

                                    

TODO
====

See github issue list - post if any needed

https://github.com/adebarbara/olpy/issues
