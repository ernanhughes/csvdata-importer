Welcome to csvdata-importer's documentation!
============================================

What is csvdata-importer
------------------------

Data Importer is a library to help import data typically from a csv file into 
database tables. Quite often you have a csv file that just needs to be imported 
for an application to do further processing.

An example would be daily quotes for a stock index.


Installation
------------


    $ pip install csvdata-importer


How to use csvdata-importer
---------------------------

.. code-block:: python

    mapping_file_path = "mapping.json"
    mapping = Mapping(load_mapping(mapping_file_path))
    inserted_col_count = Importer(str(mapping)).process()
    print("We inserted %d columns using mapping file %s",
        inserted_col_count, mapping_file_path)

It can be used to import data from a csv file to a postgres
or sqlite database.

It uses a configuration file to define how the data is mapped before it is imported to 
the database.


.. image:: img/process.jpg
   :width: 250px
   :height: 120px
   :scale: 100% %
   :alt: the process used to import data
   :align: center

The configuration file is an json document that defines the database connection, the table to import to
and the mappings



Mapping file Example
--------------------

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

.. list-table:: Columns and their function in the mapping file
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
     - The action taken on the table if it is non empty. Can be one of fail, append or replace.
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

If exists handling
------------------

The IF_EXIST configuration settling controls what happens if data exists in the target table.
fail:    will do nothing
append:  will add data tot he table
replace: will replace the contents of the table


Different types of mappings
---------------------------

DIRECT
In this case we read the value from the file and write it directly to the table row column.

CONSTANT
In this case it is a constant value and we are just updating the table with the value we find in the COLUMN_VALUE mapping.

EVALUATION
Here we are evaluating some code to create the data. The code in the COLUMN_VALUE mapping field is evaluated.



Mapping Example 1
-----------------

Here I am mapping the name column in the csv file DIRECTLY to the quote_name column in the table.

.. code-block:: json

    {
      "COLUMN_NAME": "quote_name",
      "FILE_COLUMN_NAME": "name",
      "MAPPING_TYPE": "DIRECT"
    }


Mapping Example 2
-----------------

Here I am mapping the source column in the table to a constant value. Whatever is in the file will be ignored.

.. code-block:: json

    {
      "COLUMN_NAME": "source",
      "FILE_COLUMN_NAME": "source",
      "MAPPING_TYPE": "CONSTANT",
      "CONSTANT_VALUE": "File Import"
    }


Mapping Example 3
-----------------

Here I am mapping the delta column to an evaluated value.
The value in the delta column will be the close value - the open.

.. code-block:: json

    {
      "COLUMN_NAME": "delta",
      "MAPPING_TYPE": "EVALUATED",
      "CONSTANT_VALUE": "close - open"
    }


Example mapping file
--------------------

You can download an example mapping file here:
:download:`example_mapping.json </_downloads/example_mapping.json>`


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
