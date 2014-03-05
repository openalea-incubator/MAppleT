Differences between Lpy and LStudio
====================================

While moving from MAppleT to Stocatree, the original L system had to be 
translated. Of course C++ code had to be translated as well.  Concerning the 
Lsystem syntax, the translation was quite straightforward because Lpy and LStudio
syntax are similar. Here are some differences that have been spotted, which 
could be useful to know:


* Stop() behaviour is not the same as in Lpy: does not go to the End function. 
  So the End() function must be called explicitely.
* group in Lstudio can have a name by using #define  commands. In Lpy such 
  usage is not possible and only numbers may be used as group's name
* DisplayFrame() is called frameDisplay()
* func() function in LStudio is not available in Python, but python function 
  may be used to replace it if required like in stocatree.
* original version $ symbol replace by @v in lpy 

.. warning:: avoid to use lsystem string as an argument to EndEach  Otherwise 
    this lstring will be replaced agaain and again each time iteration is perfomed
    with the consequence that it decreases the performace dramatically and
    requires huge memory (may have been fixed now). 


.. sectionauthor:: Thomas Cokelaer
