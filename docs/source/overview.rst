Overview: Data Extraction Made Simple
==============================================

``tidyextractors`` makes extracting data from supported sources as painless as possible, delivering a populated Pandas DataFrame in three lines of code. ``tidyextractors`` was inspired by `Hadley Wickham's (2014) paper <http://vita.had.co.nz/papers/tidy-data.html>`_  which introduces "tidy data" as a conceptual framework for data preparation.

Features
-----------------

* Extracts data with minimal effort.
* Creates readable code that requires minimal explanation.
* Exports Pandas Dataframes to maximize compatibility with the Python data science ecosystem.

Data Sources Implemented
------------------------------------------

``tidyextractors`` currently has submodules for extracting data from the following sources:

* Local Git Repositories
* Twitter User Data (including Tweets) using the Twitter API
* Emails stored in the ``mbox`` file format.
