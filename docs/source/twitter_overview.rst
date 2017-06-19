Twitter Data Extraction
===============================

The ``tidyextractors.tidytwitter`` submodule lets you extract user data from Twitter with minimal effort. This page will guide you through the process.

Step 1: Get API Credentials
----------------------------------

To extract data using the Twitter API, you will first need to obtain API credentials. Your API credentials contain four pieces of information:

* ``access_token``
* ``access_secret``
* ``consumer_key``
* ``consumer_secret``

To get these credentials, check out the Twitter developer documentation: https://dev.twitter.com/oauth/overview/application-owner-access-tokens

Step 2: Extract Data
-------------------------

Once you have your API credentials, you can extract user data with the ``TwitterExtractor``:

.. code-block:: python

  import tidyextractors.tidytwitter as tt

  credentials = {
    # Randomly generated example credentials for demonstration only
    'access_token': '985689236-R0EjHQJZLya6gb82R5g8Odb4UMwkhQy4Q2AxzBnB',
    'access_secret': 'CVuVV0LSf74PQt2HH6zt08aeumGdMvlZtKF7BbHvRmX4r',
    'consumer_key': 'F47AzSRag0KvVFG4eJYexuDqB',
    'consumer_secret': 'lovnyqIA1oKs0jI4A27VXLLSUWrKc0hnNzyTu39NWIjSiq1xxj'
  }

  users = ['user1','user2','user3']

  tx = tt.TwitterExtractor(users, **credentials)

Step 3: Get Data
--------------------------

You can now get your data in a number of tidy formats using either the ``get_tidy`` method:

.. code-block:: python

  user_df = tx.get_tidy('users')

  tweet_df = tx.get_tidy('tweets')

A slightly my flexible option is to call the ``TwitterExtractor`` output methods directly. This is useful if you want to include collections in the cells of your DataFrame (e.g. lists or dictionaries), which are dropped when using ``get_tidy`` because tidy data must have only atomic values.

.. code-block:: python

  user_df = tx.users()

  tweet_df = tx.tweets()

``get_tidy`` Options and Aliases
----------------------------------

As shown above, there are two format options for ``TwitterExtractor.get_tidy``. Each of these options may also use a short alias:

+--------+-------------+-------------------------------------+
| Lookup | Method Used | Example Usage                       |
+========+=============+=====================================+
| users  | users       | TwitterExtractor.get_tidy('users')  |
+--------+-------------+-------------------------------------+
| tweets | tweets      | TwitterExtractor.get_tidy('tweets') |
+--------+-------------+-------------------------------------+
| u      | users       | TwitterExtractor.get_tidy('u')      |
+--------+-------------+-------------------------------------+
| t      | tweets      | TwitterExtractor.get_tidy('t')      |
+--------+-------------+-------------------------------------+
