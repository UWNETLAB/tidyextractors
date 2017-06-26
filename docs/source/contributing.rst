Contributing
===============

``tidyextractors`` is a very new project, but it will grow quickly in the coming month. If there is a particular kind of data you are interested in extracting, or which to contribute to the package, please contact Joel Becker (`mail@joelbecker.ca <mailto:%22Joel%20Becker%22%3cmail@joelbecker.ca%3e>`_) or Jillian Anderson (jillianderson8@gmail.com) and we will respond ASAP.

Creating an Extractor
----------------------------

Contributing a new extractor is relatively simple. Broadly speaking, you need to create a submodule with an extractor class inheriting from ``BaseExtractor``. To create this class (e.g. ``NewExtractor``) you need to do the following:

* Define a ``NewExtractor._extract`` method, which should extract data and assign it to ``NewExtractor._data``. This method will be called by ``BaseExtractor.__init__`` during initialization.
* Create a method to return each data format (e.g. ``commits``, ``changes``).