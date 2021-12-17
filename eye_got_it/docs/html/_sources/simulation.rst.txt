.. _simulation:

Simulation Mode
***************

.. _simulationConfigurationWindows:

Simulation Configuration
========================

.. _simulationInit:

Simulation Init :
-----------------

.. figure:: images/simulation_config.png
   :alt: Simulation Config
   :name: simulationConfigWindows
   :width: 90.0%

   Simulation Config

In the simulation Init ( :numref:`simulationConfigWindows` ) the user can select the database, the audio
and video setting (if the user want the audio and the video) and “Allow
Eye Tracker recoding” if the user want to use an Eye Tracker.

If you want, you can test operation of the audio, video and the Eye Tracker (by checking "Allow" and select the input). See :ref:`parametersHardwareTest` in :ref:`parameters` section.

“Random text selection” can create a random list of text (with different language, level, … ). 

**Important : Calibrate Eye tracker before use it !**

.. _simulationRandomSimulation:

Random Simulation
-----------------

When the user select ”Random text selection”, new options appear (:numref:`randomSimulationWindows` )

.. figure:: images/random_simulation.png
   :alt: Random Simulation
   :name: randomSimulationWindows
   :width: 90.0%

   Random Simulation

The user can select how many texts he wants. If the database is
categorized by level, you can specify if you want a random level or
select a level of your choice for the ramdom simulation. It’s the same
for the language (if the database is categorized by language). See the
database section for more details.

.. _simulationSimulationWindows:


Simulation Windows
==================

.. _simulationStartSimulation:

Start the simulation
--------------------

.. figure:: ./images/simulation_mode.png
   :alt: Simulation Mode Windows
   :name: simulationModeWindows
   :width: 90.0%

   Simulation Mode 

In simulation mode (:numref:`simulationModeWindows`) the user can choose the language, the level (if
the database is categorized by language, level or both), then choose the
text. In random simulation, the user can only choose among the list of
text selected randomly. To display the text the user must click on the
“select” button.

The user can navigate between the pages by pressing the ’a’ and ’q’ keys
to go to the previous page and ’e’ and ’d’ for the next page.

When the user click on “start simulation”, the windows is hidden and
reappears after one second approxymately (to make sure that the
Eye Tracker is recording). A red text “Recording” appears to show the
user that the simulation is in progress. The word coordinates are saved (See :ref:`simulationWordsCoordinates` for more informations)

When the user stop the simulation (by pressing the enter key on keyboard
or by clicking on the “stop simulation” button), he can then select the
words not understood. If the simulation is in random mode, the current text is deleted from the text
list.

.. _simulationSelectWords:

Select the words not understood
-------------------------------

.. figure:: ./images/select_word.png
   :alt: Select understood word
   :name: selectWordWindows
   :width: 90.0%

   Select understood word

In this windows (:numref:`selectWordWindows`) , the user can add words not understood by selecting
it and clicking on “Add Word” (one word at a time).

If the user want to remove words not understood, the user must reselect the word and clicking on "Remove Word" (one word at a time).

When all the words are selected the user can click on “Save” and the
list of words not understood is saved in a file named ”textPart.txt”. If
a MCQ as been created for this text, a popup ask the user if he want to
do this MCQ. See :ref:`mcqAnswer` in :ref:`mcq` section.


