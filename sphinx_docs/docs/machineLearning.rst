
Machine Learning
****************

We use sklearn to create model of machine learning. See the `Sklearn Documentation <https://scikit-learn.org/stable/index.html>`__ .

We create 3 models of machine learning :

-   Decision Tree : See `Wikipedia Decision Tree <https://en.wikipedia.org/wiki/Decision_tree>`__ and `Sklearn Doc Decision Tree <https://scikit-learn.org/stable/modules/tree.html>`__ .
-   KNN : See `Wikipedia KNN <https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm>`__ and `Sklearn Doc KNN <https://scikit-learn.org/stable/modules/neighbors.html>`__ .
-   SVM : See `Wikipedia SVM <https://en.wikipedia.org/wiki/Support-vector_machine>`__ and `Sklearn Doc SVM <https://scikit-learn.org/stable/modules/svm.html>`__ .


To create a dataset, make recording in Eye Got It and generate report and clicking on Machine Learning. 
Create single "dataFrame.csv" and save it in machine_learning folder in the model folder.

Then execute python script model to generate and export model.

Place model generated (.joblib) in eye_got_it/model folder. Don't forget to edit the modelConfig.ini in eye_got_it/model folder to edit them or add them and add column needed by the model.

For KNN and SVM the .joblib exported is the model automatically optimized for best performance.
