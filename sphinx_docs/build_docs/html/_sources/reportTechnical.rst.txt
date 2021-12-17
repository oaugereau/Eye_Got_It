Report Technical
****************

.. _reportPageCreation:

-------------
Page Creation
-------------

For the "eyeTracker.csv" and "eyeTrackerHead.csv", we divide them in
multiple files "eyeTracker_*.csv" and "eyeTrackerHead_*.csv", where \* is
the current page of the text.

We also filter the data in order to keep only the valid data and to keep
only the gazes and fixations recorded after the start unix time
(everything before or after the start and end of the simulation is not
included) and if the "validity_gaze" or "validity_pos" is "valid.