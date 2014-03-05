
Performance
#####################################

Code performance
================

Stocatree is written in pure Python. Therefore, it is expected that simulations
 will be slower than those from MAppleT. In this section, we provide benchmark 
 to compare the time needed to perform simulation with stocatree and MAppleT 


Here below are the benchmark of MAppleT and Stocatree (in seconds) as a function
of simulated years. Performances are not linear because number of elements is not:


.. table:: **MAppleT/Lstudio performances**

    ========== ====== ====== ======  ======  ====== =====
    year       1      1.5    2       2.5     3      4
    ========== ====== ====== ======  ======  ====== =====
    seconds    19     25     39      60      120    343
    ========== ====== ====== ======  ======  ====== =====


.. csv-table:: **Lpy/stocatree performances**
    :widths: 40,20,20,20,20,20,20,20
    :header-rows: 1
    :stub-columns: 1
    :delim: 0x20

    year           1     1.5   2       2.5      3         3.5    4
    May/2010       2.6   7     22      70       167(3000)   x     1630
    "May/2010(no mecanics)"      1.6   5     12      39(2238) 142(2450)  x 1540(9450)
    1/Feb/2009     5     14    49      132      420        x x
    1/dec/2009     9     31    62      340      523(1059)  x 2089
    animate(Nov/10)  6.5   14    45(401)      120(2533)     332(2720)  872(9649)    x
    animate(8/10)   10.5   22    62           166           332        x            x
    animate(5/10)   25     55    171          400           990        x            x


.. 5 years = 250 minutes 18000 elements.
.. depends on number of elements, for instance for 2.5 year, here are the time (y) and elements  number(x)
.. y = [74.3, 74.4, 67, 87, 67, 73, 72, 67, 83, 76, 101, 90,75, 64, 79, 71, 82, 75, 80, 73, 71.5]
.. x [2471, 2386, 2246, 3058, 2232, 2407, 2460, 2152, 2880, 2669, 3490, 3125, 2560, 2042, 2611, 2247, 2758, 2400, 2647, 2189, 2349]



.. length of axial tree = [58,273,422,2575,8553, 8609]
.. lpy = numpy.array([2.6, 7.5, 24, 77, 217, 593, 1451])    #217 for len(lstring)=2575


.. plot::
    :include-source:

    import numpy
    import pylab
    years = numpy.array([1,1.5,2,2.5,3,4])
    mapplet = numpy.array([19.,25.,39.,60.,120.,343.])
    lpy = numpy.array([2.6, 7.5, 24, 77, 217, 1451])
    lpy2 = numpy.array([9.5, 15, 40, 120, 340, 1990])
    fig = pylab.plot(years, mapplet, years, lpy, 'or-',years, lpy2,'x-' )
    l = pylab.legend(['mapplet','lpy run','lpy animate'],loc='best')
    pylab.xlabel('Simulated years'); 
    pylab.ylabel('Simulation duration (s)') 

.. plot::


    import numpy
    import pylab
    years = numpy.array([1,1.5,2,2.5,3,4])
    mapplet = numpy.array([19.,25.,39.,60.,120.,343.])
    lpy = numpy.array([2.6, 7.5, 24, 77, 217, 1451])
    lpy2 = numpy.array([9.5, 15, 40, 120, 340, 1990])
    fig = pylab.semilogy(years, mapplet,years, lpy, 'or-', years, lpy2,'x-')
    l = pylab.legend(['mapplet','lpy run','lpy animate'],loc='best')
    pylab.xlabel('Simulated years (log scale)'); 
    pylab.ylabel('Simulation duration (s)') 

.. plot::

    import numpy
    import pylab
    pylab.matplotlib.rc('font', size=13)
    years = numpy.array([1,1.5,2,2.5,3,4])
    mapplet = numpy.array([19.,25.,39.,60.,120.,343.])
    lpy = numpy.array([2.6, 7.5, 24, 77, 217, 1451])
    lpy2 = numpy.array([9.5, 15, 40, 120, 340, 1990])
    #fig = pylab.plot(years, lpy/mapplet, 'or-', years, lpy2/mapplet, 'x-')
    fig = pylab.plot(years, lpy2/mapplet, 'x-', label='L-Py/LPFG')
    #pylab.legend(['L-Py / LPFG', 'L-Py (anim)/LPFG'],loc='best')
    pylab.legend(loc='best')
    pylab.xlabel('Simulated years' )
    pylab.ylabel('Ratio computational time')
    pylab.grid()
    l, pos = pylab.xticks()
    pylab.xticks(l, ['1(60)','1.5(275)','2(425)','2.5(2600)','3(8600)', '3.5','4'], rotation=20)


.. sectionauthor:: Thomas Cokelaer
