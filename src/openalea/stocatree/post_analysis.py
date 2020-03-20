#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
.. topic:: post_analysis.py summary

    Module that implements functions that create graphical output
    given the standard stocatree outputs.

    :Code: mature
    :Documentation: mature
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id: fruit.py 8635 2010-04-14 08:48:47Z cokelaer $
    
    
.. deprecated:: 0.9.3
"""



import datetime
import numpy
import pylab
from pylab import datestr2num, num2date
import matplotlib.dates as mdates




def trunk_radius(filename):
    """Read the trunk.dat and create output graphics

    :param tag: if tag is provided the file that will be read is trunk_<tag>.dat
    """
    #load the data (date format for the first column)
    
    data = numpy.loadtxt(filename, converters={0:pylab.datestr2num})
    dates = numpy.array(pylab.num2date(data[:,0]))

    #plot the results
    fig = pylab.figure()
    ax = fig.add_subplot(111)
    ax.plot(dates, data[:,2]*100)  # multiply by 100 to get centimeters


    #set axis locators

    if dates.min().year==dates.max().year:
        years    = mdates.YearLocator()   # every year
        yearsFmt = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(yearsFmt) # set major ticks to the years
        ax.xaxis.set_major_locator(years)
    else:
        years    = mdates.YearLocator()   # every year
        yearsFmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_formatter(yearsFmt) # set major ticks to the years
        ax.xaxis.set_major_locator(years)

    datemin = datetime.date(dates.min().year, dates.min().month, dates.min().day)
    datemax = datetime.date(dates.max().year, dates.max().month, dates.max().day)

    ax.set_xlim(datemin, datemax)

    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    fig.autofmt_xdate()
    pylab.grid(True)
    pylab.ylabel('Trunk radius (cm)')
    pylab.xlabel('Time (years)')
    pylab.show()


if __name__=='__main__':
    tag='test'
    trunk_radius(tag)
