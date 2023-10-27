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


Installation
------------


    $ pip install data-importer


Data Importer
-------------

A configurable file to database table importer.
It can be used to import data from a csv file to a postgres
or sqlite database.

You build a mapping json file and then use that to create or update tables
on the database.

.. image:: img/process.jpg
   :width: 250px
   :height: 120px
   :scale: 100% %
   :alt: the process used to import data
   :align: center



Mapping file Example
-------

.. code-block:: json
    {
        "DATABASE_URL": "postgresql://user:pwd@host:5432/db",
        "TARGET_TABLE": "quote",
        "IF_EXISTS": "append",
        "COLUMN_MAPPING": [
            {
              "COLUMN_NAME": "source",
              "FILE_COLUMN_NAME": "source",
              "MAPPING_TYPE": "CONSTANT",
              "CONSTANT_VALUE": "test-data"
            },
            {
              "COLUMN_NAME": "quote_value",
              "FILE_COLUMN_NAME": "close",
            }
        ]
    }

Importing data using the mapping file
-------------------------------------

The overall mapping configuration

.. list-table:: Columns and their function inf the mapping file
   :widths: 20 30 50
   :header-rows: 1

   * - Column Name
     - Example
     - Description
   * - DATABASE_URL
     - postgresql://user:pass@host:5432/db
     - The database we are connecting to
   * - TARGET_TABLE
     - quote
     - The table in that database we are updating or creating
   * - FILE_PATH
     - /test.csv
     - The file we are importing
   * - IF_EXISTS
     - append
     - The action taken on the table if it is non empty. Can be one of fail, append.
   * - COLUMN_MAPPING
     - array of columns see next table
     - The columns and how they are mapped

The column mappings

.. list-table:: Columns mappings
   :widths: 20 30 50
   :header-rows: 1

   * - Column Name
     - Example
     - Description
   * - COLUMN_NAME
     - quote_value
     - The table column we are updating
   * - FILE_COLUMN_NAME
     - quote
     - The column in the csv we are reading from
   * - MAPPING_TYPE
     - DIRECT
     - The type of mapping we are doing. See below
   * - COLUMN_VALUE
     - File Import
     - For use when we are evaluating or mapping a constant to the table.


Different types of mappings
---------------------------

DIRECT
In this case we read the value form the file and write it directly to the table row column.

CONSTANT
In this case it is a constant value and we are just updating the table with the value we find in the CONSTANT_VALUE mapping.

EVALUATION
Here we are evaluating some code to create the data.




.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
