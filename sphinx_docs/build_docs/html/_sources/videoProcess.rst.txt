.. _VideoProcessing:

Video processing
================

.. _openFace:

--------
OpenFace
--------

We used openFace in report to process the video (see the `OpenFace
Wiki <https://github.com/TadasBaltrusaitis/OpenFace/wiki>`__).

.. figure:: images/openFace.png
   :alt: Openface Interface
   :name: openFaceInterface
   :width: 90.0%

   Openface Interface

When we are in report mode, we don’t use the graphic interface (:numref:`openFaceInterface`) but the
command line in terminal :
``FeatureExtraction.exe -f " + inputVideo + " -out_dir " + outputVideo``.

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
aligned faces from the video (:numref:`openFaceAlignedFaceTec` ).


.. figure:: images/openFaceScreenshot/frame_det_00_000001.jpg
   :alt: Video Aligned face
   :name: openFaceAlignedFaceTec
   :width: 25.0%

   Video Aligned face

The "video.hog" (:numref:`openFaceHogTec`) is written as a binary file (for
space consideration) and can be read by matlab script for example.

.. figure:: images/openFaceScreenshot/hog_features.png
   :alt: Hog file
   :name: openFaceHogTec
   :width: 25.0%

   Hog file

The "video.avi" video file show image peer image the
head and eyes position in 3D space (:numref:`openFaceVideoTec`)

.. figure:: images/openFaceScreenshot/vlcsnap-2021-05-11-14h50m15s383.png
   :alt: Video processed
   :name: openFaceVideoTec
   :width: 50.0%

   Video processed

**CSV File**

**Source : openFace Wiki**

*Basic*:

frame : the number of the frame (in case of sequences)

face_id : the face id (in case of multiple faces), there is no guarantee
that this is consistent across frames in case of FaceLandmarkVidMulti,
especially in longer sequences.

timestamp : the timer of video being processed in seconds (in case of
sequences).

confidence : how confident is the tracker in current landmark detection
estimage.

success : is the track successful (is there a face in the frame or do we
think we tracked it well).

*Gaze related*:

gaze_0_x, gaze_0_y, gaze_0_z : Eye gaze direction vector in world
coordinates for eye 0 (normalized), eye 0 is the leftmost eye in the
image (think of it as a ray going from the left eye in the image in the
direction of the eye gaze).

gaze_1_x, gaze_1_y, gaze_1_z : Eye gaze direction vector in world
coordinates for eye 1 (normalized), eye 1 is the rightmost eye in the
image (think of it as a ray going from the right eye in the image in the
direction of the eye gaze).

gaze_angle_x, gaze_angle_y : Eye gaze direction in radians in world
coordinates averaged for both eyes and converted into more easy to use
format than gaze vectors. If a person is looking left-right this will
results in the change of gaze_angle_x (from positive to negative) and,
if a person is looking up-down this will result in change of
gaze_angle_y (from negative to positive), if a person is looking
straight ahead both of the angles will be close to 0 (within measurement
error).

eye_lmk_x_0, eye_lmk_x_1,... eye_lmk_x55, eye_lmk_y_1,... eye_lmk_y_55 : location of 2D eye region landmarks in pixels. The landmark index can be
found below

eye_lmk_X_0, eye_lmk_X_1,... eye_lmk_X55, eye_lmk_Y_0,... eye_lmk_Z_55 : location of 3D eye region landmarks in millimeters. The landmark index
can be found below

.. image:: images/openFaceScreenshot/eye_lmk_markup.png
   :alt: image
   :width: 80.0%

*Pose*:

pose_Tx, pose_Ty, pose_Tz : the location of the head with respect to
camera in millimeters (positive Z is away from the camera).

pose_Rx, pose_Ry, pose_Rz : Rotation is in radians around X,Y,Z axes with
the convention R = Rx \* Ry \* Rz, left-handed positive sign. This can
be seen as pitch (Rx), yaw (Ry), and roll (Rz). The rotation is in world
coordinates with camera being the origin.

Lines in au intensities and au occurrences correspond to predicted
Action Unit presence and intensities respectively. For more details see
here.

Where the landmarks are no longer in pixel values but in millimetres and
we also report head pose and gaze (this however needs accurate estimates
of fx,fy,cx,cy. This functionality is useful for batch image processing
where the camera is the same and we want to know pose and gaze.

*Landmarks locations in 2D*:

x_0, x_1, ... x_66, x_67, y_0,...y_67 location of 2D landmarks in
pixels.

*Landmarks locations in 3D*:

X_0, ... X_67, Y_0,...Y_67, Z_0,...Z_67 location of 3D landmarks in
millimetres.

.. image:: images/openFaceScreenshot/landmark_scheme_68.png
   :alt: image
   :width: 50.0%

*Rigid and non-rigid shape parameters*:

Parameters of a point distribution model (PDM) that describe the rigid
face shape (location, scale and rotation) and non-rigid face shape
(deformation due to expression and identity).

p_scale, p_rx, p_ry, p_rz, p_tx, p_ty - scale, rotation and translation
terms of the PDM.

p_0, p_1, ... p_33 - non-rigid shape parameters.

*Facial Action Units*:

Facial Action Units (AUs) are a way to describe human facial expression,
more details on Action Units can be found here
https://en.wikipedia.org/wiki/Facial_Action_Coding_System .

The system can detect the intensity (from 0 to 5) of 17 AUs:

AU01_r, AU02_r, AU04_r, AU05_r, AU06_r, AU07_r, AU09_r, AU10_r, AU12_r,
AU14_r, AU15_r, AU17_r, AU20_r, AU23_r, AU25_r, AU26_r, AU45_r

And the presense (0 absent, 1 present) of 18 AUs:

AU01_c, AU02_c, AU04_c, AU05_c, AU06_c, AU07_c, AU09_c, AU10_c, AU12_c,
AU14_c, AU15_c, AU17_c, AU20_c, AU23_c, AU25_c, AU26_c, AU28_c, AU45_c


.. _openCV:

------
OpenCV
------

If openFace is not detected (is not possible because it is installed in
the same folder as Eye got It), openCv is used in place.

It create a video file named "video_processed.avi" and contain the video
with eyes and head graphic positions represented by blue and green
rectangles. (:numref:`opencvVideo`).

.. figure:: images/vlcsnap-2021-05-11-15h14m32s687.png
   :alt: video precessed
   :name: opencvVideo
   :width: 50.0%

   video precessed

Two csv files are created : "eyes.csv" (:numref:`eyesCSV` ) and "face.csv" (:numref:`faceCSV`) and
contain coordinates of the eyes and the face, the video time and the
current number image.


.. table:: eyes.csv File example
   :name: eyesCSV

   ====== == == ===== ====== ==============
   number x  y  width height time
   ====== == == ===== ====== ==============
   1      60 35 23    23     0:00:00.033333
   4      60 34 21    21     0:00:00.133333
   10     56 32 21    21     0:00:00.333333
   17     58 31 22    22     0:00:00.566667
   20     61 32 22    22     0:00:00.666667
   24     62 31 23    23     0:00:00.800000
   ====== == == ===== ====== ==============


.. table:: face.csv File example
   :name: faceCSV
   
   ====== === === ===== ====== ==============
   number x   y   width height time
   ====== === === ===== ====== ==============
   1      98  116 112   112    0:00:00.033333
   4      102 117 108   108    0:00:00.133333
   6      104 120 106   106    0:00:00.200000
   10     106 119 103   103    0:00:00.333333
   11     104 120 105   105    0:00:00.366667
   12     101 118 109   109    0:00:00.400000
   ====== === === ===== ====== ==============

