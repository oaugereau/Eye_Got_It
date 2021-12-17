.. _report:

***********
Report Mode
***********

.. figure:: images/report_config.png
   :alt: Report Config
   :name: reportConfigWindows
   :width: 90.0%

   Report Config Windows

In the Report Mode (:numref:`reportConfigWindows`) the user can select the user, the session and the record for wich
he want to create a report. 
The user can generate only one report or all report in the session of the user. Same with the Eye Tracker algorithm and Machine learning.

If "Open the folder at the end" is selected, the report folder will be
opened when the generation of the report is finished.

If the user want to regenerate all the report, it can select "delete folder before report". If it doesn't want or just want to update the report, the user must not select it.   

If you want to process the action units, you can check them and edit them with the button "Check Action Units". For more information, please see :ref:`actionUnits` section.

.. _reportDataProcessing:

Data Processing
===============

.. _reportEyeTracker:

-----------
Eye Tracker
-----------

.. figure:: images/EyeTracker_0.jpg
   :alt: EyeTracker
   :name: eyeTrackerScreenshot
   :width: 90.0%

   EyeTracker

To create gazes and fixations (:numref:`eyeTrackerScreenshot`) we use the Buscher and Nystrom algorithm. For
more information go to the :ref:`eyeTrackerAlgo` in :ref:`eyeTracker` section.

.. _reportWordsCoordinates:

-----------------
Words coordinates
-----------------

.. figure:: images/Word_Page_0.jpg
   :alt: Word Coordonate
   :name: wordCoordonateScreenshot
   :width: 90.0%

   Word Coordonate

We export for each page the words position (:numref:`wordCoordonateScreenshot`).

.. _reportVideoProcessing:

----------------
Video Processing
----------------

In the output folder, four files are created and one folder as well :

-  video_aligned/

-  video.avi

-  video.csv

-  video.hog

-  video_of_details.txt

video_of_details.txt content :

.. code:: default

   Input:webcam
   Camera parameters:500,500,320,240
   Output HOG:video.hog
   Output video:video.avi
   Output aligned directory:video_aligned
   Output csv:video.csv
   Gaze: 1
   AUs: 1
   Landmarks 2D: 1
   Landmarks 3D: 1
   Pose: 1
   Shape parameters: 1

The folder "video_aligned/" contain the extraction of
aligned faces from the video (:numref:`openFaceAlignedFace` ).


.. figure:: images/openFaceScreenshot/frame_det_00_000001.jpg
   :alt: Video Aligned face
   :name: openFaceAlignedFace
   :width: 25.0%

   Video Aligned face

The "video.hog" (:numref:`openFaceHog`) is written as a binary file (for
space consideration) and can be read by matlab script for example.

.. figure:: images/openFaceScreenshot/hog_features.png
   :alt: Hog file
   :name: openFaceHog
   :width: 25.0%

   Hog file

The "video.avi" video file show image peer image the
head and eyes position in 3D space (:numref:`openFaceVideo`).

.. figure:: images/openFaceScreenshot/vlcsnap-2021-05-11-14h50m15s383.png
   :alt: Video processed
   :name: openFaceVideo
   :width: 50.0%

   Video processed

For more information about video processing, see :ref:`VideoProcessing` .

.. _reportActionUnits:

------------
Action Units
------------

The action Units detected are saved in the "action_units" folder in "video_processed" folder in the report folder, it contains all the emotions detected and all Video Aligned face corresponding.

For more information, please see :ref:`actionUnits` section.

.. _reportExportReport:

-------------
Export Report
-------------

At the end of the report, a file named "Report.txt" is created. It
contain all the informations about the simulation, the MCQ answer with a score and more informations like the
time read, the user informations, ...

.. dropdown:: Click to view an Example

   .. code:: default

      Report : 2021_04_23_09_19_11

      Screen Resolution :
         Screen width : 1920
         Screen heigth : 1080

      Offset coordinate :
         x0 : 277
         y0 : 215

      User : 
         Name : Yoda Master
         Birthday : 26/4/1200
         Genre : Male
         Level : C2
         Toeic : 1000
         Country : Galaxy far, far away

      User Data : 
      Audio : True
      Video : True
      EyeTracker : True

      Text : 
      Title : A_Happy_Visitor.Beginner.txt
      Page Read : 3

      Time Read : 
      Page 0 : 42884
      Page 1 : 31153
      Page 2 : 2817

      UNIX Time : 
      Start : 1619162358158
      Page 0 : 1619162401042
      Page 1 : 1619162432195
      Stop : 1619162435012


      UNIX Time Start 
      Start Audio : 1619162358569
      Start Video : 1619162358307
      Start Eye Tracker Eye : 1619162358180
      Start Eye Tracker Head: 1619162358167

      Video : 
         Time video : 0:01:16.500000
         Size video : 320x240
         FPS : 30.0
         Total Frame : 2295

      MCQ : 

      QUESTION 1 : What is at the door of the house?
      USER ANSWER : a dog
      RIGHT ANSWERS

      QUESTION 2 : What happens at the end of the story?
      USER ANSWER : Anna keeps the dog.
      RIGHT ANSWERS

      QUESTION 3 : Is the dog dry or wet?
      USER ANSWER : The dog is wet.
      RIGHT ANSWERS

      QUESTION 4 : What day of the week is it in the story?
      USER ANSWER : Thursday
      RIGHT ANSWERS

      Score : 10.0/10