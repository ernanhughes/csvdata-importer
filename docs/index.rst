.. data-importer documentation master file, created by
sphinx-quickstart on Tue Oct 24 08:59:29 2023.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

Welcome to data-importer's documentation!
=========================================

What is data-importer
---------------------
Data Importer is a libray to help move csv file into database tables.
Quite often you have a csv file that just needs to be imported for an application to do further processing.

An example would be daily quotes for a stock index.

.. image:: img/process.jpg
   :width: 250px
   :height: 120px
   :scale: 100% %
   :alt: the process used to import data
   :align: right


.. code-block json

{
    "DATABASE_URL": "postgresql://stock_prediction:stock_prediction@localhost:5432/stock_prediction",
    "TARGET_TABLE": "quote",
    "IF_EXISTS": "append",
    "COLUMN_MAPPING": [
        {
            "COLUMN_NAME": "name",
            "FILE_COLUMN_NAME": "name",
            "EVAL": "",
            "MAPPING_TYPE": "DIRECT",
            "REQUIRED": "True",
            "CONSTANT_VALUE": "",
            "type": "TEXT",
            "nullable": true,
            "autoincrement": false,
            "comment": null,
            "default": null
        },
        {
            ....
        }
    ]
}


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
