What is Tidy Data?
========================

`Hadley Wickham (2014) <http://vita.had.co.nz/papers/tidy-data.html>`_ introduced "tidy data" to describe data that has been cleaned and reshaped in a way that is ready for analysis. The concept of tidy data inspired ``tidyextractors``, which provides a convenient interface for extracting data in a tidy format. However, what is a tidy format?

Our Definition of Tidy Data
---------------------------------

We consider data to be "tidy" if it satisfies the following constraints:

* Data values are atomic. No cell contains a collection of items (e.g. a list, set, or dictionary).
* Each row is a single observation. This is to say that each row represents a single "entity" (e.g. such as a commit, a change to a file, or a tweet) which can be uniquely identified by a primary key (e.g. MessageID for an email, or MessageID and recipient for an email "send").
* Each column is a single variable.

This definition intentionally allows for a certain degree of data redundancy, which would be eliminated in traditional database normalizations, such as BCNF.

Choosing Output Formats
-----------------------------------

We have a few guiding principals for deciding which output formats to implement for a given extractor:

* If an entity would have its own table in a normalized database, it should be available as an output format.
* Dataset should include all variables that have meaningful information about the table's defining unit of observation, even if this data may be redundant between rows.
* In general, more data is preferred to less data, so long as it is meaningful. It is easier to drop data than to integrate data.

Not Your Grandfather's Tidy Data
------------------------------------

If you are familiar with Hadley's paper, you may notice that our definition is different from his. We did this because we find the original definition to be self-contradictory. Hadley claims that tidy data is "Codd’s 3rd normal form, but with the constraints framed in statistical language, and the focus put on a single dataset rather than the many connected datasets common in relational databases." However, Codd's 3rd normal form `requires` multiple tables.

We agree with Hadley's claim that single table datasets are optimal for data analysis. We also agree with his practice of preferring single datasets at the cost of some data redundancy. We feel that our definition of tidy data is in the spirit of Hadley's original paper.
