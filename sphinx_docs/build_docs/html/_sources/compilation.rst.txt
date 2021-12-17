.. _compilation:


Compilation
***********

Before Compilation
==================

-  Make sure that the new version not containing any bug =) .
-  Edit the ChangeLog with the new version and new feature.
-  Edit the version number and set the initial_setup to "True" in the "config.ini" file (see :ref:`parametersConfigFile`).
-  Create a backup named config.ini.bak (It will loaded if the config.ini is corrupted). 
-  Edit if necessary the Pyinstaller script "Main.spec" to add new files/folders or hidden dependencies.
-  Please edit the MyAppVersion to the new Eye Got It version and the Location if necessary in the Innot Setup script (setup.iss). 
-  Don't forget to edit the documentation version and copy build documentation in Eye Got It documentation folder (See :ref:`documentation` for more informations).

.. _compilationEXE:

Generate an exe file
====================

To generate an exe file, we use pyinstaller. Please see the :ref:`requirementPyinstaller` in :ref:`requirementCompilation` section for the installation.

We created a spec file of Main.py called Main.spec (see at the end of this page).

Inside we declare the pathex, the file data, please see the `docs html <https://pyinstaller.readthedocs.io/en/stable/>`__ or the `doc pdf <https://readthedocs.org/projects/pyinstaller/downloads/pdf/stable/>`__ .

To create an exe file run ``pyinstaller Main.spec`` or if you are multiple python version : ``py -X.X -m pyinstaller Main.spec`` (where X.X is the python version).

If you error during the compilation, try to remove the build folder.

After that you will have two folders created :

Eye Got It

-  build => compilation.

-  dist => exe file result of the compilation.

.. dropdown:: Click to view the pyinstaller script

   .. literalinclude:: /files/Main.spec
      :linenos:
      :name: exeCode
      :caption: Pyinstaller Code

.. _compilationInstaller:

Generate an Installer
=====================

To create an installer for windows, we use Inno Setup. Please see the in :ref:`requirementInnoSetup` in :ref:`requirementCompilation` section to install it.

We created an ISS file to create an installer (we create the script by using the Inno Setup "Script Wizard").

IMPORTANT : **Please test the installation and the Eye Got It before publishing a new release on the git.**

The compilation created the installer in the folder Output in the Eye Got It folder.

For more information : see `the Inno Setup documentation <https://jrsoftware.org/ishelp/>`__.


.. dropdown:: Click to view the Inno Setup Script

   .. literalinclude:: /files/setup.iss
      :linenos:
      :name: installerCode
      :caption: Inno Setup Code


Error python import
===================

If you add new python dependency, during the compilation to EXE File, Pyinstaller not imported all module (experimented with sklearn, with some hidden dependencies ). You can add the hidden import in the hiddenimports in Pyinstaller script (Main.spec).