.. _parameters:

**********
Parameters
**********

.. _parametersParametersWindows:

Parameters Windows
==================

In the parameters window (see :numref:`parameters-windows-screenshot` ), the user can edit the output files name for the eyeTracker, audio, video and report files.

All parameters are saved in config.ini (see :ref:`simulationConfig` section).

**Important : All modification of file name will be applied only for the next recording.**

.. _parameters-windows-screenshot:
.. figure:: ./images/parameters_windows.png
   :alt: Parameters Window
   :width: 70.0%

   Parameters Window

.. _parametersConfigFile:

Configuration file
==================

All parameters in the parameters window are saved in the config.ini file.


Initial setup
-------------

The Initial setup is when the user run Eye Got for the first time. A popup inform the user that the initial setup is done, then, it can restart Eye Got It.

For more information about Eye Got It, see :ref:`compilationInstaller` in :ref:`compilation` section.


Action Units
============

Please see :ref:`actionUnits` section.

.. _parametersHardwareTest:

Hardware Test
=============

.. _parametersAudioTest:

Audio Test
----------

In the Sound test window (see :numref:`audio-test-screenshot`), the user can select the input for the
audio and test it. The user can also change the audio parameters.

The audio is not saved into an audio file.

.. _audio-test-screenshot:
.. figure:: ./images/audio_test.png
   :alt: Audio Test Windows
   :width: 70.0%

   Audio Test Windows

.. _parametersVideoTest:

Video Test
----------

When the user select the "Video Test" button, a new window is displayed
and show the webcam output. The user can stop the display by closing the
window or by pressing "q" or "enter" on the keyboard. This window only show the
webcam output and doesn’t record anything.


.. _parametersEyeTrackerTest:

Eye Tracker Test
----------------

In the Eye Tracker Test, you cant check if the Eye Tracker is correctly calibrated (See :numref:`eyeTracker-test-screenshot`). 

When you click on the "start" button, tle lines are hiding before to be showing, the test is started. You can stop the test by click on the "stop" button or press the "ENTER". 
The Eye tracker Gazes are displayed on the windows. For more information about the Eye Tracker test, please see the :ref:`eyeTracker` section.

When you close the windows the temporary Eye Tracker data are deleted.

.. _eyeTracker-test-screenshot:
.. figure:: ./images/eyeTrackerTestCalibration.png
   :alt: Eye Tracker Test Calibration
   :width: 100.0%

   Eye Tracker Test Calibration
