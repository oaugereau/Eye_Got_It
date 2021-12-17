.. _documentation:

Documentation
*************

For the HTML documentation, we use Sphinx (`See Sphinx website <https://www.sphinx-doc.org/en/master/>`__).

The documentation are saved in *sphinx_docs* folder. To build it the the make file : ``.\make html`` for html and ``.\make latexpdf`` for pdf (latex compilator must be installed).

The sphinx documentation is written in reStructuredText , see the `Sphinx documentation <https://www.sphinx-doc.org/en/master/contents.html>`__ for more informations.

Edit documentation version in config.py and make a copy of build_docs/html to eye_got_it/docs/html when build the doc to add the last version in Eye Got It (when you clicking on help button).

If file or new page not including when you build, try to remove build_docs folder then rebuild the documentation.