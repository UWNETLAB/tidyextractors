tidyextractors
=================

Overview
-----------------

``tidyextractors`` makes extracting data from supported sources as painless as possible, delivering you a populated Pandas DataFrame in three lines of code. ``tidyextractors`` was inspired by `Hadley Whickham's (2014) paper <http://vita.had.co.nz/papers/tidy-data.html>`_  which introduces "tidy data" as a conceptual framework for data preparation.

Features
-----------------

* Extracts data with minimal effort.
* Creates readable code that requires minimal explanation.
* Exports Pandas Dataframes to maximize compatibility with the Python data science ecosystem.

A Quick Example
-----------------

You can use the ``GitExtractor`` to quickly extract a record of commits or changes from a local Git repository. For example, this is what happens when you run the following code within the ``tidyextractors`` repository:

::

  import tidyextractors.tidygit as tg
  gx = tg.GitExtractor('')
  pandas_data = gx.get_tidy('changes')

The result is a Pandas DataFrame where each row is a committed change to a specific file. To fit this page, we'll just look at a few columns using ``pandas_data[['hash','file','author_email','summary','changes/insertions']]``:

+-----------+-------------------------------------------+----------------------+-----------------+--------------------+
| hash      | file                                      | author_email         | summary         | insertions         |
+===========+===========================================+======================+=================+====================+
| 'd85fab4' | 'tidyextractors/tidygit/__init__.py'      | 'mail@joelbecker.ca' | 'Removed im...' |                  1 |
+-----------+-------------------------------------------+----------------------+-----------------+--------------------+
| '743a777' | 'tidyextractors/base_extractor.py'        | 'mail@joelbecker.ca' | 'Fixed _dro...' |                 69 |
+-----------+-------------------------------------------+----------------------+-----------------+--------------------+
| '743a777' | 'tidyextractors/tidygit/git_extractor.py' | 'mail@joelbecker.ca' | 'Fixed _dro...' |                  9 |
+-----------+-------------------------------------------+----------------------+-----------------+--------------------+
| 'add9794' | 'tidyextractors/base_extractor.py'        | 'mail@joelbecker.ca' | 'Fixed one ...' |                 15 |
+-----------+-------------------------------------------+----------------------+-----------------+--------------------+
| '44ec7f6' | 'tidyextractors/base_extractor.py'        | 'mail@joelbecker.ca' | 'Added rena...' |                  6 |
+-----------+-------------------------------------------+----------------------+-----------------+--------------------+

Installing
-----------------
In the near future, ``tidyextractors`` will be distributed on PyPI and accessible via ``pip``. For now, clone the repository and run ``pip install -e .`` in the cloned directory.

Currently Implemented Data Sources
-----------------

* Local Git Repositories

Near Future Data Sources
-----------------

* Twitter User Data (including Tweets) using the Twitter API
* Emails stored in the ``mbox`` file format.

Contributing
-----------------

``tidyextractors`` is a very new project, but it will grow quickly in the coming month. If there is a particular kind of data you are interested in extracting, or which to contribute to the package, please contact Joel Becker (`mail@joelbecker.ca <mailto:%22Joel%20Becker%22%3cmail@joelbecker.ca%3e>`_) or Jillian Anderson (jillianderson8@gmail.com) and we will respond ASAP.
