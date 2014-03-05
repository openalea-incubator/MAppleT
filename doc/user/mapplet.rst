
MAppleT notes
################

"*MAppleT project aimed to bring together models of topology and geometry in a single simulation such that the architecture of an apple tree may emerge from process interactions. This integration was performed using L-systems. A mixed approach was developed based on stochastic models to simulate plant topology and mechanistic model for the geometry. The succession of growth units (GUs) along axes and
their branching structure were jointly modelled by a hierarchical hidden Markov model. A biomechanical model, derived
from previous studies, was used to calculate stem form at the metamer scale, taking into account the intra-year dynamics of
primary, secondary and fruit growth. Outputs consist of 3-D mock-ups – geometric models representing the progression of
tree form over time. To asses these models, a sensitivity analysis was performed and descriptors were compared between
simulated and digitised trees, including the total number of GUs in the entire tree, descriptors of shoot geometry (basal
diameter, length), and descriptors of axis geometry (inclination, curvature). In conclusion, despite some limitations,
MAppleT constitutes a useful tool for simulating development of apple trees in interaction with gravity.*" [ref1]_


Running MAppleT
===============

MAppleT is written in C++. It also provides a Lsystem, which can be launch in L-Studio. 
The original code of MAppleT is available in the directory **./src/cpp.** where the original 
code written by Colin Smith was committed in the archive in January 2007. In order to use the code, 
one's need to compile it and therefore to have third-party libraries (for statistical analysis, VPlants.Stat_Tool). 
In the original code, a fork of VPlants.Stat_tool and VPlants.Sequence_analysis was required. This fork
is not available anymore. However, by changing the input files (e.g. fmodel_fuji_16_65_y3_96.txt), 
the current code of VPlants.Stat_tool and VPlants.Sequence_Analysis seems to work. Therefore, there 
is no need to use the fork anymore and the current version of MAppleT can be linked with the i
current version of VPlants (Dec 2009).

.. topic:: compilation note

    Under Windows, one should first install VPlants and then change the header within the cpp/hpp files.

    Then, use the **go.bat** script. You may need to change the Makefile according to your environments.

.. warning:: See the **description.txt** file in ./src/cpp for extra information, 
    in particular about compilation and L-studio version to be used

.. note:: Modifications of the original code (e.g. the headers) was required to 
    allow the compilation to work with VPlants. In addition, the input data files 
    had matrices with zero columns that prevent the code to run. The modifications
    were committed in Nov 2009.


.. sectionauthor:: Thomas Cokelaer
