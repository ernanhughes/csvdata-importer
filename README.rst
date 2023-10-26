data-importer
=============

Documentation
-------------

https://data-importer.readthedocs.io


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


Mapping file Example
-------

.. code-block:: json

    {
        "DATABASE_URL": "postgresql://user:pwd@host:5432/db",
        "TARGET_TABLE": "quote",
        "IF_EXISTS": "append",
        "COLUMN_MAPPING": [
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
   * - CONSTANT_VALUE
     - File Import
     - For use when we are mapping a constant to the table.


Different types of mappings
---------------------------

DIRECT
In this case we read the value form the file and write it directly to the table row column.

CONSTANT
In this case it is a constant value and we are just updating the table with the value we find in the CONSTANT_VALUE mapping.


