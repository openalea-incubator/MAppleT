Stocatree quick start
######################



Installation
==============
Sources are available from the `SVN <https://gforge.inria.fr/scm/viewvc.php/vplants/trunk/MAppleT/?root=vplants>`_. 
Once the source are downloaded, the package can be installed by typing::

    python setup.py install

If you do not have the access to the SVN, you can still get a released version
or source code from the main page project of vplants (see `Openalea wiki <http://openalea.gforge.inria.fr>`_)

.. topic:: dependencies and cython

    Stocatree requires the following packages:

    * VPlants.Stat_tool, VPlants.Sequence_analysis, 
    * Vplants.PlantGL
    * OpenAlea.Mtg.
    * Vplants.Plantik
    * Scipy/numpy/Matplotlib

    Note that there is also a Cython module, which goal is to make the code
    faster. It should compile and install automatically using the command above. 

In order to test if the installation worked properly, open a python shell and 
type::


    from openalea.stocatree import *
    a = apex_data()

Using Stocatree within Lpy
=============================

Stocatree modules are used to assemble a model within a Lsystem, so what you want
to do first is to run this Lsystem. You can find the script **stocatree.lpy** 
in **./share/data/** and starts the **Lpy** application to run it.

Load the **stocatree.lpy** script from Lpy and press Run

.. warning:: the plotting will slow down the computation as soon as the second year is reached. There is no need to look at the graphical output at every step, so we advice to use the Step iteration options and set it to 800, which corresponds to one season roughly speaking.

.. note:: This documentation does not provide any help about LPy, you should look
    at the `VPlants.LPy <http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/vplants.html>`_ 
    documentation instead.

Using Stocatree as a python script
==================================


You can run Stocatree Lsystem from a python shell. Under Linux, we advice you 
to use **ipython**  with the **-q4thread** option (to use the PlantGL Viewer)::

.. code-block:: bash

    ipython -q4thread

then, import the relevant modules::

    import openalea.lpy as lpy
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from openalea.stocatree import get_shared_data

Read the **lpy** file and iterate through the simulation::

    l = lpy.Lsystem(get_shared_data('stocatree.lpy'))
    N = int(2900*2) # fix the number of iterations
    res = l.iterate(1)
    res = l.iterate(1,N,res)

and finally, plot the results::

    app = QApplication([])
    l.plot(res)

The previous code should render as follows

.. plot:: 

    from openalea.stocatree import get_shared_data
    import openalea.lpy as lpy
    #from PyQt4.QtCore import *
    #from PyQt4.QtGui import *
    l = lpy.Lsystem(get_shared_data('stocatree.lpy'))
    N = int(2900*1.8) # fix the number of iterations
    res = l.iterate(1)
    res = l.iterate(1,N,res)
    #app = QApplication([])
    l.plot(res)
    from vplants.plantgl.all import Viewer
    Viewer.frameGL.saveImage('user/test.png')


.. image:: test.png
    :width: 480px
    :height: 480px

Playing with the configuration
===============================


The are many options that can be changed such as the time step, rendering colors,
leaf size, tropism and so on. All these options are stored in a configuration 
file called **stocatree.ini**, which must be found in the same directory as the 
lsystem (in our case ./share/data). This file can be edited to fulfill your needs. 
(see reference guide, :mod:`~openalea.stocatree.config_doc`, for more details).

.. sectionauthor:: Thomas Cokelaer
