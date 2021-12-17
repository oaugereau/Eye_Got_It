.. _EyeVoiceSpan:

Eye-voice Span
**************

.. _eyeVoiceSpanTheory:


Eye-voice Span : Theory and explanation
=======================================

An effective way to evaluate the cognitive process of reading a text aloud during the simulation (or multiple texts with different difficulty levels for that matter) is to determine the variation of the eye-voice span or EVS. 

EVS is the distance between eye and voice and typically we usually find that the eye leads over voice position. Studying the variation of this distance during the reading process can be a strong indicator of linguistic proficiency and also an accurate predictor of the durations of eye fixations (more than word frequency or even word length) (`Laubrock J. <https://loop.frontiersin.org/people/204143/overview>`__ , `Kliegl R. <https://loop.frontiersin.org/people/9008/overview>`__ 2015).

.. figure:: images/An-example-of-the-method-used-to-measure-the-eye-voice-lead-is-reported-for-a-typically_W640.jpg
   :alt: Example of Eye-Voice lead in a typically developed reader
   :name: EVS
   :width: 100.0%

   An example of the method used to measure the eye-voice lead is reported for a typically developed reader. Figure was uploaded by Pierluigi Zoccolotti.


The eye-voice span has been used in a study published in the Frontiers in Human Neuroscience (De Luca M., Pontillo M., Primativo S., Spinelli D, Zoccolotti P. 2013) to evaluate the eye-voice lead in dyslexic individual compared to typically developed readers. The study listed compelling data backing and confirming early observations by Buswell (1921) and Fairbanks (1937) that the EVS was, in fact, significantly smaller in dyslexic than control readers with greater number of silent pauses alongside an increased number of eye fixations.


Although our use case is different from the study’s as previously mentioned, the use of EVS and determining its variation during a simulation will give us theoretically a concrete and deterministic parameter to evaluate a language proficiency level. And, since we already have successfully extracted the fixations and saccades from the eye gaze input data, the next step will be to analyse these fixations and the recorded voice together and determine the actual EVS variation.


In the next sections, we will discuss the tools that we used to evaluate the eye-voice span and how we integrated this feature into the existing application, the final results that we obtained and an overall discussion and critiques.


References:
^^^^^^^^^^^

Laubrock J, Kliegl R. The eye-voice span during reading aloud. Front Psychol. 2015;6:1432. Published 2015 Sep 24. doi:10.3389/fpsyg.2015.01432

De Luca M, Pontillo M, Primativo S, Spinelli D, Zoccolotti P. The eye-voice lead during oral reading in developmental dyslexia. Front Hum Neurosci. 2013;7:696. Published 2013 Nov 6. doi:10.3389/fnhum.2013.00696

Buswell G. T. (1921). The relationship between eye-perception and voice-response in reading. J. Educ. Psychol. 12, 217–227 10.1037/h0070548 [CrossRef] [Google Scholar]

Tiffin J., Fairbanks G. (1937). An eye-voice camera for clinical and research studies. Psychol. Monogr. 48, 70–77 [Google Scholar]


.. _implementation:

Implementation
==============


To calculate the EVS and its variation during the reading simulation, it is important to first determine the necessary input(s) that we will need and any data processing steps along the way.

The actual EVS implementation can be divided into two main, distinct steps:


-  Aligning the recording from the simulation with the text being read so to fix the duration during which the individual is reading each pronounced word.

-  Associating each fixation already calculated with the corresponding word from the text being read. 


We will first begin by introducing the third-party service that we will be using for the audio-text alignment named MAUS, its principal and overall premise and then move on to explaining the algorithm that we developed and eventually integrated in the application.


.. _MAUS:

MAUS
====

What is MAUS?
^^^^^^^^^^^^^

Munich Automatic Segmentation System is a tool developed in the Technical University in Munich used to automatically find the correlation between linguistic categories (e.g., word, syllable, phone) and corresponding signals (e.g., acoustic signal, spectrum, articulatory signal, neuronal signals)	and segment the latter accordingly.
`official documentation <https://www.bas.uni-muenchen.de/Bas/BasMAUS.html>`__ .


The aim from MAUS
^^^^^^^^^^^^^^^^^

It was developed to allow the segmentation large amounts of data in a relatively short time to allow research and development in the areas of speech processing to be faster and more efficient without having to listen and manually segment the signals.


How it works
^^^^^^^^^^^^


MAUS require a text and an audio file as inputs. The text input part will go through two transformations:

-  The first is the normalization: remove all punctuation and numbers within the text.

-  The second is the pronunciation: modify the text according to the expected pronunciation when reading the text. Words are now phonemes i.e.  "please" becomes "pli:z".


Then, depending on the audio file, the program will calculate all the possible pronunciation variants and generate a probability graph of these variants.


As a final step, MAUS will look for this path between the phonetic part that are expected and maximize it with the acoustic probabilities.


.. figure:: images/Example-of-a-segmentation-labeling-created-by-MAUS.png
   :alt: Example of MAUS automatic segmentation
   :name: MAUSExample
   :width: 100.0%

   Example of MAUS automatic segmentation `Original Source <https://infolux.uni.lu/automatic-phonetic-segmentation-for-luxembourgish/>`__



For faster results we will be using the MAUS web service where the input files are uploaded to the BAS CLARIN server, processed by MAUS and the result returned to the local computer.

**Important**
Note that MAUS is free to use for all individuals. However, it is very much not extensible or by any means not modifiable.  Thus, the result that we will later on mention will be strongly correlated with the precision and accuracy of this system.


.. _evsAlgorithm:

EVS algorithm
=============

To determine the eye-voice span variation, we followed the steps depicted in the figure down bellow and explained in detail afterwards.

.. figure:: images/documentation_EVS.png
   :alt: Steps to generate EVS Graph
   :name: StepsEVS
   :width: 100.0%

   Steps to generate EVS Graph

To integrate the Eye-voice span feature’s code in the existing application, we created a separate class called “EVS” (in EVSGeneration.py) to encapsulate this functionality and to preserve the modularity of the original source code.  

The goal of our class is to generate a graph depicting the EVS variation in time to assess how comfortable the individual is at reading and understanding a certain language. 

This class will be called when the user generates the report corresponding to a specific simulation.

Now let's go into a more detailed code review:

The launch of the entire process is done within the constructor when the “EVS” class is called.

At this point, the algorithm requires several input variables, which are the following: 


-  The .txt file that has been read during the simulation.
-  The audio file recorded during the simulation.


After an initialization, the constructor will directly call the "generateGraphLearning" function, this function will take care of the entire process of generating the final graph. 

The following is a detailed explanation of the needed steps that allow us to generate the EVS graph: 

First of all, we start by associating each fixation detected and retained during the simulation with the word(s) in the corresponding word. This way, we can deduce at the specific moment which word is actually being looked at by the user.

To do so we needed to fetch and use:


- The coordinates of the pixel at the top left of the rectangle that encompasses each word as well as its height and width (from textPosition.csv).

.. figure:: images/box.jpg
   :alt: BoxWord
   :name: BoxWord
   :width: 60.0%

   Rectangles encompasing words


-  The coordinates of the centre of each fixation and the timestamp corresponding to this fixation in Milliseconds.

.. figure:: images/fix.jpg
   :alt: fix
   :name: fix
   :width: 60.0%

   Coordinates of the center of each given fixation

From the coordinates of the centre of each fixation, we go through all the bounding boxes of the words of the text read and we check whether the centre of this fixation is located inside one of these boxes.

If this is the case, then the word is associated with the corresponding fixation and therefore a specific period of time. This way, we can automatically eliminate stray fixations resulting from a sudden change in eye movement. 

To be able to use this data in the final step of our work, we finish this algorithm by saving the data obtained in a csv file “Visualization”. For each page read, we generating the corresponding “Visualization” csv file. Every fixation-word association is given a index that will help us later on with determining the EVS.


.. container:: center

   .. table:: visualization.csv Example
      :name: visualizationExample

      +----------+---------------------+---------------+-------+
      |   word   |  time               | duration_ms   | id    | 
      +----------+---------------------+---------------+-------+
      |   see    | 0.0,166547          | 166547        | 71    | 
      +----------+---------------------+---------------+-------+
      | TV       | 0.22000000000025466 | 133238        | 21    | 
      +----------+---------------------+---------------+-------+
      | is       | 0.3830000000002656  | 799425        | 2     | 
      +----------+---------------------+---------------+-------+
      | Thursday | 1.2150000000001455  | 999281        | 3     | 
      +----------+---------------------+---------------+-------+
      | Thursday | 2.481999999999971   | 266475        | 3     | 
      +----------+---------------------+---------------+-------+
      | is       | 2.780999999999949   | 399712        | 5     | 
      +----------+---------------------+---------------+-------+

.. _evsResultsObservation:

EVS results
===========

The "generateTextGrid” function which will call the MAUS webservice which, after injecting our audio file and the read txt file, will return a response file in textgird format which contains audio snippets with words from the text read during the simulation.

After having retrieved all this information in lists via the "getData" function, we have the necessary data to generate the final graph. The "generateDataGraph" function will check if a word has been looked at in the time interval when the user says a word. If this is the case, we add to our list a map listing the word read, the word seen, the moment and the number of words in advance between the word said and seen using the index field added.

This map is then passed to the "generateGraph" function, which will generate the EVS variation graphs in time for a chosen simulation and saves them a pngs in the corresponding report folder.

.. figure:: images/evs_folder.PNG
   :alt: Folder Containing generated EVS graphs and cvs files
   :name: FolderEVS
   :width: 60.0%

   Folder Containing generated EVS graphs and cvs files

.. figure:: images/graph_evs.png
   :alt: An exemple of generated EVS graph
   :name: EVSGraphExample
   :width: 100.0%

   An exemple of generated EVS graph 

.. _evsObservationDiscussion:

EVS observations et discussion
==============================

In order to test of the application thoroughly, we’ve decided that we have to analyse in depth the results of MAUS web service as well as the post processing we apply to find the EVS values.

MAUS Accuracy and Stability evaluation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First test: Mismatched text and audio files
-------------------------------------------

After sending Mismatched text and audio file to the Web Service, we observed that, firstly, we did not get any errors or warnings from the service and a textgrid file was successfully generated. 
Here we have the comparison between a text and an audio not corresponding on the top and corresponding text and audio with the good audio on the bottom. 

.. figure:: images/evs-graph-wrong-audio.png
   :alt: evs with wrong audio text
   :name: EVSWrongAudio
   :width: 100.0%

   EVS graph Mismatched audio and text

.. figure:: images/evs-graph-right-audio.png
   :alt: evs graph right audio text
   :name: EVSGraphRightAudio
   :width: 100.0%

   EVS graph with correctly corresponding audio and text


In spite of results that seemed coherent on the obtained Textgrid file we can observe that the calculation of the EVS shows that there was a problem because there should be an equal number of points between the two graphs.

As we analysed the textgrid even further, the file looked like a “normal” file, in the sense that it had no apparent inconsistencies and words were successfully associated with an interval of. 

After using MAUS's viewer tool for the TextGrid, only then we were able to see the results were incorrect. In fact, even with mismatch input files, MAUS “forces” the alignment of text with the audio without any actual association between audio signal and phenomes.

This observation suggests that MAUS is not always reliable if the individual makes lot of pauses reading the text or if an error occurs and an entirely different audio file is instead sent (which is in our case highly unlikely but it is very important to note). 


Second Test: Stuttering on certain words or repeating certain words completely
------------------------------------------------------------------------------

For this test, we intentionally sent to the MAUS web service, two recordings made by the same person and on the same text but during one of the recordings the person made sure to stutter on some words or fully repeat them. 

The graph on the top represents the text read with stuttering and the text on the bottom represents the text read normally. 

.. figure:: images/graph-evs-stutter.png
   :alt: graph evs stutter
   :name: evsStutter
   :width: 100.0%

   EVS Graph with stutter

.. figure:: images/graph-evs-no-stutter.png
   :alt: graph evs no stutter
   :name: evsNoStutter
   :width: 100.0%

   EVS Graph without stutter

We can notice that, on the top image, when the person stutters on the words we manage to have an EVS which passes to zero whereas, on the bottom image, the EVS is higher on average and does not pass by 0. 






**Developers**:

This feature was developed by Nicolas MENUT, Marine LE GALL et Asma NAIFAR - 2021.
