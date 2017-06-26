Git Repository Data Extraction
===============================

The ``tidyextractors.tidygit`` submodule lets you extract Git log data from a local Git repository. This page will guide you through the process.


A Minimal Code Example
------------------------------

.. code-block:: python

  from tidyextractors.tidygit import GitExtractor

  # Extract data from a local Git repo
  gx = GitExtractor('./your/repo/dir/')

  # Commit data in a Pandas DataFrame.
  commits_df = gx.commits(drop_collections=True)

  # Commit/file keyed change data in a Pandas DataFrame
  changes_df = gx.changes()

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

Now, you can call a ``GitExtractor`` method to return data in a Pandas DataFrame.

.. code-block:: python

  # Commit data in a Pandas DataFrame.
  commits_df = gx.commits(drop_collections=True)

  # Commit/file keyed change data in a Pandas DataFrame
  changes_df = gx.changes()

.. note::

    ``GitExtractor.commits()`` drops columns with collections of data in cells (i.e. ``list``, ``set``, and ``dicts``) because "tidy data" requires only atomic values in cells.
    If you don't want data dropped, change the ``drop_collections`` argument to false.