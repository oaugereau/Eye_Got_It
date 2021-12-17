# Welcome to the Eye_Got_It Project

<p align="center">
<img src="eye_got_it/Pictures/eye_got_it.png"  style="width:70.0%" alt="Logo" />
</p>

For full documentation, see the sphinx documentation 
in sphinx_docs/build_docs/html/index.html.

IMPORTANT : Use the testing branch for Eye Got It developpment. When new release is done, push in the Main branch `git push -f origin testing:main`

# Requirement

## Python

### Eye Got It


| Module        | Version used | Website                                 |
|---------------|--------------|-----------------------------------------|
| Python        | 3.9.4        | https://www.python.org/                 |
| configparser  | 5.0.2        | https://pypi.org/project/configparser/  |
| matplotlib    | 3.4.1        | https://pypi.org/project/matplotlib/    |
| numpy         | 1.20.2       | https://pypi.org/project/numpy/         |
| opencv-python | 4.5.1.48     | https://pypi.org/project/opencv-python/ |
| PyAudio       | 0.2.11       | https://pypi.org/project/PyAudio        |
| PyQt5         | 5.15.4       | https://pypi.org/project/PyQt5/         |
| scikit-learn  | 0.24.2       | https://pypi.org/project/scikit-learn/  |
| pygrabber     | 0.1          | https://pypi.org/project/pygrabber/0.1/ |


You can run (if python is already installed) run Init.py to check if all
python dependency are installed.

### Doumentation

| Module                           | Version used | Website                                        |
|----------------------------------|--------------|------------------------------------------------|
| Sphinx (for doc)                 | 4.0.2        | https://pypi.org/project/Sphinx/               |
| sphinx-rtd-theme (theme for doc) | 0.5.2        | https://pypi.org/search/?q=sphinx-rtd-theme&o= |
| sphinx-panels                    | 0.6.0        | https://pypi.org/project/sphinx-panels/        |

### Package installation

To install this package, we use :

| Module     | Version used | Website                              |
|------------|--------------|--------------------------------------|
| pip        | 21.1         | https://pypi.org/project/pip/        |
| pip-review | 1.1.0        | https://pypi.org/project/pip-review/ |
| pipwin     | 0.5.1        | https://pypi.org/project/pipwin      |

**Important** : The version of python dependencies is only the version
available when we developed Eye Got It.

Example : `pip install PyQt5` .

**Important** : If you have any problem to install Pyaudio, try this:

-   `pip install pipwin`
-   `pipwin install PyAudio`

We use pyinstaller to compile python project in .exe .

## Eye Tracker Requirement

For the Eye Tracker we use 2 SDK provide by Tobii :

-   Interaction Library for gaming Eye Tracker.
-   SDK Pro for pro and research Eye Tracker.

### Interaction Library

We use Visual Studio (2019 version) for the Interaction Library c++ code
:   Please see <https://visualstudio.microsoft.com/fr/> .

To compile the c++, we used the Visual Studio Build Tools (2019
version).

For more informations, please see the Eye Tracker section in the
documentation or 
[Interaction Library website](https://developer.tobii.com/product-integration/interaction-library/getting-started/).

### SDK pro

Like SDK Pro is only compatible with python 3.6 (at the moment), you
must install python 3.6 if you want to edit and test the script.

To use with python 3.9, we create an exe file. Please see the
documentation.

For more informations, please see the Eye Tracker section in the
documentation or [Tobii SDK Pro website](http://developer.tobiipro.com/).

## Compilation

### Pyinstaller

To generate an exe file for python code, we use Pyinstaller :

| Module      | Version used | Website                               |
|-------------|--------------|---------------------------------------|
| pyinstaller | 4.3          | https://pypi.org/project/pyinstaller/ |

We create a spec pyinstaller file for create the exe file, please see
the compilation section in the documentation for more information.

### Inno Setup

We use also Inno Setup to create an .exe instaler for windows
(<https://jrsoftware.org/isinfo.php>).

For more Information, please see the compilation section in the
documentation.

## OpenFace

For Video processing, we used OpenFace (See
[Website](https://github.com/TadasBaltrusaitis/OpenFace)).

Just open and extract openFace.exe in eye_got_it OpenFace folder (we
create a compressed part file due to GitHub limit file size).
