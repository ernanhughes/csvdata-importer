data-importer
==========

Documentation
-------------

https://data-importer.readthedocs.io


Installation
------------


    $ pip install data-importer



Data Importer
-----------

A configurable file to database table importer. 
It can be used to import data from a csv file to a postgres or sqlite database. 


data-importer
----------

Based on CheckedDict, a data-importer is a persistent, unique dictionary. It is
saved under the config folder determined by the OS and it is updated with each
modification. It is useful for implementing configuration of a module / library
/ app, where there is a default/initial state and the user needs to be able to
configure global settings which must be persisted between sessions (similar to
the settings in an application)

Example
-------

.. code-block:: python

   config = data-importer("myproj.subproj")
   config.addKey("keyA", 10, doc="documentaion of keyA")
   config.addKey("keyB", 0.5, range=(0, 1))
   config.addKey("keyC", "blue", choices=("blue", "red"),
                 doc="documentation of keyC")
   config.load()

Alternatively, a data-importer can be created all at once:

.. code-block:: python
                
   config = data-importer("myapp",
       default = {
           'font-size': 10.0,
           'font-family': "Monospace",
           'port' : 9100,
       },
       validator = {
           'font-size::range' : (8, 24),
           'port::range' : (9000, 65000),
           'font-family::choices' : {'Roboto', 'Monospace'},
       },
       docs = {
           'port': 'The port number to listen to',
           'font-size': 'The size of the font, in pixels'
       }
   )

This will create the dictionary and load any persisted version. Any saved
modifications will override the default values. Whenever the user changes any
value (via ``config[key] = newvalue``) the dictionary will be saved.

In all other respects a data-importer behaves like a normal dictionary.
