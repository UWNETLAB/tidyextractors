Git Repository Data Extraction
===============================

The ``tidyextractors.tidygit`` submodule lets you extract Git log data from a local Git repository. This page will guide you through the process.


A Minimal Code Example
------------------------------

.. code-block:: python

  from tidyextractors.tidygit import GitExtractor

  # Extract data from a local Git repo
  gx = GitExtractor('./your/repo/dir/')

  # Commit data in a Pandas DataFrame
  commits_df = gx.get_tidy('commits')

  # Commit/file keyed change data in a Pandas DataFrame
  changes_df = gx.get_tidy('changes')

Step 1: Prepare Your Git Repo
----------------------------------

All you need to get started is the path to any local Git repository. If you want to extract data from a repository hosted on GitHub, download or clone the repository to your computer.

Step 2: Extract Data
-------------------------

You can extract data from any local Git repository using the ``GitExtractor``:

.. code-block:: python

  from tidyextractors.tidygit import GitExtractor

  gx = GitExtractor('./your/repo/dir/')

You may need to wait while the data is being extracted, but all the data is now stored inside the extractor object. You just need a bit more code to get it in your preferred format.

Step 3: Get Pandas Data
--------------------------

You can now use the ``get_tidy`` method to get a Pandas ``DataFrame`` in the tidy format of your choice.

.. code-block:: python

  commits_df = gx.get_tidy('commits')

  changes_df = gx.get_tidy('changes')

A slightly my flexible option is to call the ``MboxExtractor`` output methods directly. This is useful if you want to include collections in the cells of your DataFrame (e.g. lists or dictionaries), which are dropped when using ``get_tidy`` because tidy data must have only atomic values.

.. code-block:: python

  commits_df = gx.commits()

  changes_df = gx.changes()

``get_tidy`` Options and Aliases
----------------------------------

As shown above, there are two format options for ``GitExtractor.get_tidy``. Each of these options  also use a short alias:

+---------+-------------+----------------------------------+
| Lookup  | Method Used | Example Usage                    |
+=========+=============+==================================+
| commits | commits     | GitExtractor.get_tidy('commits') |
+---------+-------------+----------------------------------+
| changes | changes     | GitExtractor.get_tidy('changes') |
+---------+-------------+----------------------------------+
| cm      | commits     | GitExtractor.get_tidy('cm')      |
+---------+-------------+----------------------------------+
| ch      | changes     | GitExtractor.get_tidy('ch')      |
+---------+-------------+----------------------------------+
