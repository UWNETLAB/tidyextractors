Mbox Data Extraction
===============================

Mbox is a file format used to store mailbox data on Unix operating systems. The ``tidyextractors.tidymbox`` submodule lets you extract user data from Mbox files with minimal effort. This page will guide you through the process.

A Minimal Code Example
------------------------------


.. code-block:: python

  from tidyextractors.tidymbox as MboxExtractor

  # Extracts all mbox files in this directory.
  mx = MboxExtractor('./your/mbox/dir/')

  # Email messages in a Pandas DataFrame.
  email_df = mx.get_tidy('emails')

  # MessageID/receiver keyed Pandas DataFrame.
  sends_df = mx.get_tidy('sends')

Step 1: Prepare Your Mbox Files
----------------------------------

You can extract data from a single Mbox file, or multiple Mbox files. However, all these files must be in a single directory:

.. code-block:: bash

  ls -1 ./your/mbox/dir/
  file1.mbox
  file2.mbox
  file3.mbox

Step 2: Extract Data
-------------------------

Once you have consolidated your Mbox files, you can extract data from them using the ``MboxExtractor``:

.. code-block:: python

  from tidyextractors.tidymbox as MboxExtractor

  # All mbox files in the directory
  mx = MboxExtractor('./your/mbox/dir/')

  # Only one mbox file
  mx = MboxExtractor('./your/mbox/dir/file1.mbox')

You may need to wait while the data is being extracted, but all the data is now stored inside the extractor object. You just need a bit more code to get it in your preferred format.

Step 3: Get Pandas Data
--------------------------

You can now use the ``get_tidy`` method to get a Pandas ``DataFrame`` in the tidy format of your choice.

.. code-block:: python

  email_df = mx.get_tidy('emails')

  sends_df = mx.get_tidy('sends')

A slightly more flexible option is to call the ``MboxExtractor`` output methods directly. This is useful if you want to include collections in the cells of your DataFrame (e.g. lists or dictionaries), which are dropped when using ``get_tidy`` because tidy data must have only atomic values.

.. code-block:: python

  email_df = mx.emails()

  sends_df = mx.sends()

``get_tidy`` Options and Aliases
----------------------------------

As shown above, there are two format options for ``MboxExtractor.get_tidy``. Each of these options may also use a short alias:

+--------+-------------+----------------------------------+
| Lookup | Method Used | Example Usage                    |
+========+=============+==================================+
| emails | emails      | MboxExtractor.get_tidy('emails') |
+--------+-------------+----------------------------------+
| sends  | sends       | MboxExtractor.get_tidy('sends')  |
+--------+-------------+----------------------------------+
| e      | emails      | MboxExtractor.get_tidy('e')      |
+--------+-------------+----------------------------------+
| s      | sends       | MboxExtractor.get_tidy('s')      |
+--------+-------------+----------------------------------+

.. note::

    This submodule's internals were adapted from Phil Deutsch's
    `mbox-to-pandas <https://github.com/phildeutsch/mbox-analysis>`_ script with his permission.
