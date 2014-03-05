#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: read_function.py summary

    facilities to read L-studio data set

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$ 

.. testsetup::

    from openalea.stocatree.tools.read_function import *
"""


def _getdata(line, key):
    assert line.startswith(key)
    res = line.split(' ')[1].replace('\n','')
    return res

class _FSet(object):
    def __init__(self, name=None, samples=100, flip=False, x=None, y=None):
        if flip=='off':
            self.flip = False
        elif flip=='on':
            self.flip = True
        else:
            raise ValueError("flip must be either 'on' or 'off' %s provided" % flip)
        self.x = x
        self.y = y
        self.name = name
        self.samples = samples
        assert len(x)==len(y)

    def __str__(self):
        output = 'name: %s\n' % self.name
        output+= 'samples: %s\n' % self.samples
        if self.flip == False:
            output+= 'flip: off\n'
        else:
            output+= 'flip: on\n'
        output+= 'points: %s\n' % len(self.x)
        for x,y in zip(self.x, self.y):
            output+= '%s %s\n' % (x, y)
        return output

def _readFunction(filename='functions.set', func_name=None, x=0):
    """Function to read a functions.fset file according to L-studio syntax given
    a function name . It returns the f(x) value (interpolated).

    .. warning:: for developers only. This function is used by :class:`ReadFunction` class, 
        which should be used by users.

    **From lpgf user guide**

    Function-set file specifies functions of one variable. The functions are defined
    as **B-spline** curves constrained in such a way that they assign exactly one y
    to every x in the normalized function domain [0, 1].

    **from cpfg user guide**

    A function specification file defines a function as a spline curve which the first
    control point's x coordinate is equal to 0, and the last point's x coordinate is
    equal to 1; in addition, for any two control points pi and pi+1, xpi
    <= xpi+1. This last condition ensures that the spline curve defines a function.
    Function specification files usually have extension .func. The format of the

    files format is::

        range: 0.0 1.0
        points: n
        x1 y1
        x2 y2
        ...
        xn-1 yn-1
        xn yn

    Here, n is the number of control points (at least 4), where point pi is (xi, yi).

    Version 1.01 The new version of the function specification adds a name, the
    number of samples which should be precomputed by cpfg (rather than calculated
    each time accessed), and an option flip, which defines whether the
    independent variable is displayed horizontally or vertically by the function editor.
    The format is::

        fver 1 1
        name: name
        samples: number of samples to precompute
        flip: on | off
        points: number of points
        x1 y1
        x2 y2
    """
    try:
        fdata = open(filename, 'r')
    except:
        IOError('Could not read filename %s', filename)

    #skipe first line
    fdata.readline()
    # get number of items
    items = int(_getdata(fdata.readline(), 'items'))

    fsets = []
    for item in range(0,items):
        # skip fver
        fdata.readline()
        name = _getdata(fdata.readline(), 'name')
        samples = float(_getdata(fdata.readline(), 'samples'))
        flip = _getdata(fdata.readline(), 'flip')
        points = int(_getdata(fdata.readline(), 'points'))
        datax = []
        datay = []
        for i in range(points):
            data = fdata.readline().split(' ')

            if float(data[0]) not in datax:
                datax.append(float(data[0]))
                datay.append(float(data[1]))

        fset = _FSet(name=name, samples=samples, flip=flip,x=datax, y=datay)

    fdata.close()

    return '', fset



class ReadFunction():
    """Read a L-studio functions.fset file, extract a func_name
    and returns interpolated values.

    :Example:

    Starting from a file like::

        funcgalleryver 1 1
        items: 2
        fver 1 1
        name: _fruit_mass
        samples: 100
        flip: off
        points: 4
        0.000000 0.000000
        0.586364 0.000000
        0.586364 0.250000
        1.000000 0.250000
        fver 1 1
        name: _leaf_area
        samples: 100
        flip: off
        points: 6
        0.000000 0.000000
        0.250000 0.100000
        0.500000 0.500000
        0.500000 0.500000
        0.750000 0.900000
        1.000000 1.000000



    we use the following code to extract the *leaf_area* data::

        >>> func = ReadFunction('functions.fset', 'leaf_area')
        >>> func.gety(0.5)
    """
    def __init__(self, filename, func_name):
        """
        :param filename: the filename with the extension
        :param func_name: the function name to extract
        """
        dummy, self.fset = _readFunction(filename, func_name, 0 )
        self.x = self.fset.x
        self.y = self.fset.y
        self.length = len(self.x)

    def gety(self, x):
        """returns the y values corresponding to x

        Use scipy and its simplest 1D interpolation method..

        :param x: the input x value
        :returns y: the interpolated y value derived from the function read in the constructor.

        ::

            x.gety(0.5)
        """
        if x<=0: return self.y[0]
        if x>=1: return self.y[self.length-1]
        index = 0
        for i, this in enumerate(self.x):
            if x>this:
                index = i
            else:
                break
        newy = self.y[index] + (self.y[index+1]-self.y[index])/(self.x[index+1]-self.x[index]) * (x-self.x[index])
        return newy
