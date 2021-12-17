.. _simulationTec:

Simulation Technical
********************

Text Adaptation
===============

This function separate the text in multiple pages that can all fit in
our application window and it also generate a rectangle around each
words so that we can know the x and y location of each of them in the
text.

The parameters of the function or:

-  metrics: We use QFontMetrics of pyqt5 to know the size in pixels that
   each word occupy.

-  text: it is the text we want to adapt to the application.

-  width: the width in pixel of the QTextEdit that hold our text.

-  height: the height in pixel of the QtextEdit that hold our text

This function is a giant loop that goes through each character. For each
character we check if the width of the line is bigger than the width of
the application, if so we add a line break and put the word that the
character was in at the start of the next line. We also check if the
character is below the bottom of the QtextEdit, if so the precedent
words are added to a page and the word that the character was in is set
as the start of the next page. When the character is a line space or a
line break that mean the end of a word so we attach coordinates, width
and height to the word.


.. _simulationWordsCoordinates:

Words Coordinates
=================

When you start a simulation, the words coordinates are saved in a csv
file : ”textPosition.csv” (:numref:`wordsFilesExample`).

.. container:: center

   .. table:: textPosition.csv File example
      :name: wordsFilesExample

      ======== === == ===== ====== ====
      Word     x   y  width height page
      ======== === == ===== ====== ====
      It       5   40 17    80     0
      is       30  40 17    80     0
      Thursday 55  40 107   80     0
      It       173 40 17    80     0
      is       198 40 17    80     0
      raining  223 40 74    80     0
      today    307 40 66    80     0
      ======== === == ===== ====== ====


.. _simulationConfig:

Simulation Config
=================

When the user stop the simulation, a file named ”config.ini” is created
in the simulation folder in the user folder.

In this file, there are informations about the simulation like the name
of the text, the number of page. It contain the unix time of the start
and the end of the simulation, the unix time when the user change a page
and the unix time of start of the audio and the video.



This file is use later when report is created (see :ref:`reportExportReport` in :ref:`report` for more informations).