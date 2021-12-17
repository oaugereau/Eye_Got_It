.. _database:

********
Database
********

.. _databaseCreate:

Create Database
===============

Before you create a database you must create a folder in your Database
Folder. Inside it you must created another folder and put all your texts
inside.

Normaly the database folder looks like :

-   Database

-   New Database

    -   Text folder

You can then click on the "Database" button in the Home windows then
"Database Gestion" and finally "add database".

Now choose the new database that you want to add (:numref:`database_create_empty`) :

.. figure:: ./images/database_create_empty.png
   :alt: Create Database
   :name: database_create_empty

   Create Database

Text name rules :

-  If your text file name contain only the title, you must enter only
   the name of the folder tha containing the texts.

-  If your text file name contain the title and language or level (or
   both), you must enter the name of the folder, the separator and the
   languages or levels (or both).

For the language and level you must separate them by "," (order is not
important) :

-  For language "en,fr,es" is the same as "fr,es,en" or "es,en,fr" or
   "es,en,fr".

-  For level : "0,1,2,3,4" is the same as "1,2,3,4,0" or "2,3,4,0,1", …

The separator can be ".", "_" or others. They separate the title, the
language and the level. The order is not important.

Example :

-  "title_language_level.txt" same as "language_level_title.txt or

   "level_title_language.txt" or "level_language_title.txt".

-  "title.language.level.txt" same as "language.level.title.txt" or

   "level.title.language.txt" or "level.language.title.txt".

In summary :

.. container:: center

   ==================== ====== ====== ====== ======
   \                    Type 1 Type 2 Type 3 Type 4
   ==================== ====== ====== ====== ======
   text folder          x      x      x      x
   separator (optional)        x      x      x
   language (optional)         x             x
   level (optional)                   x      x
   ==================== ====== ====== ====== ======

In this example the database is categorized by level (0,1,2,3,4) and
separate by "_" (:numref:`database_create_example`).

.. figure:: ./images/database_create_example.png
   :alt: Create Database Example
   :name: database_create_example

   Create Database Example

When your configuration is done, you can save by clicking on the "save"
button.

.. _databaseEdit:

Edit Database
=============

.. figure:: ./images/database_create_edit.png
   :alt: Edit Database
   :name: database_edit

   Edit Database

The database view and edit (:numref:`database_edit`) is the same that database creation.

.. _databaseConfigFile:

Database config file
====================

When you create or edit a database, a "config.ini" file is created or
edited. It contain all the informations about the database.

For the example above, the "config.ini" looks like :

::

       [DATABASE]
       separator = _
       folder = Folder Texts
       
       [LANGUAGE]
       language = 
       
       [LEVEL]
       level = 0,1,2,3,4
