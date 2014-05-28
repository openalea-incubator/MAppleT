#!/usr/bin/env python
#-*- coding: utf-8 -*-
# The "directory" arguments and attributes were added by Han on 19-04-2011
# to store the output results under the directory as designated
"""
.. topic:: namespace_output summary

    Module that provides functionalities to write stocatree outputs

    :Code: in progress
    :Documentation: in progress
    :Author: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    :Revision: $Id$
    :Usage: >>> from openalea.stocatree.output import *

.. testsetup::

    from openalea.stocatree.output import *

"""
import datetime
import os.path as op

output_options = {
    'sequences' : True,
    'l_string'  : True,
    'light_interception' : True,
    'counts'    : True,
    'trunk'    : True,
    'leaves'    : False,
    'mtg'       : True}



class output(object):
    """A base class to manage outputs in stocatree.

    This base class allows to define a filename given a basename and a tag
    and then to open/close this file easily.

    It also defines the frequency and period at which data has to be saved.

    Given a frequency, the period is computed as 365./frequency.

    This class also stored the time elapsed since the beginning.

    :param filename: a valid basename (e.g. 'output' in output.txt)
    :param verbose: True/False
    :param frequency: a frequency to save the data
    :param tag: a tag for the filename


    """
    # The "directory" parameter was added by Han on 17-04-2011
    # to allow saving the output files to an designated directory
    def __init__(self, directory='', filename=None, verbose=False, frequency=1., tag=None):
      self.file = None
      self.basename = filename
      self.directory = directory
      self.tag = tag
      self.filename = None
      self.build_filename()

      self.verbose = verbose
      self.frequency = frequency
      self.elapsed = datetime.timedelta(0)
      #by product
      self.period = 365.0 / self.frequency


    #The build_filename() method was rewritten by Han on 19-04-2011
    def build_filename(self, extra=None):
      """
      create the filename given an optional extra suffix that is used before the tag
      """
      self.filename = self.basename
      if (extra != None) and (extra != ''):
        self.filename += '_' + extra

      if self.tag:
        self.filename += '_'+self.tag

      self.filename += '.dat'

    def init(self):
      """open the file object"""
      if self.file == None or self.file.closed:
        if self.verbose:
          print 'opening file %s' % self.filename
        self.file = open(op.join(self.directory, self.filename), 'w')
      else:
        if self.verbose:
          print 'File already openned !! Close it first.'

    def close(self):
      """close the file object"""
      if self.file:
        if self.verbose:
          print 'Closing file %s ' % self.filename
        self.file.close()
        self.file= None

    def advance(self, dt):
      """increment the elapsed time and return True if time has reached a period

      :param dt: the time increment
      """
      if type(dt) != datetime.timedelta:
        dt = datetime.timedelta(dt)
      self.elapsed += dt
      if self.elapsed.days >= self.period:
        self.elapsed = datetime.timedelta(0.)
        return True
      else:
        return False


    def save(self):
      """output must have a save method to write the date into the file"""
      raise NotImplementeError()


class trunk(output):
    """Defines the output filename to store trunk information"""

    def __init__(self, directory='', filename="trunk", frequency=365., verbose=False, tag=None):
        output.__init__(self, directory=directory, filename=filename, verbose=verbose, tag=tag)

    def save(self, date, trunk_radius, trunk_cross_sectional_area):
        self.file.write("%s\t%d\t%s\t%s\n" % (date, self.elapsed.days,trunk_radius,trunk_cross_sectional_area))

class counts(output):
    """Store the count of shoots (long, small, ...)"""

    def __init__(self, directory='', filename="counts", frequency=4., verbose=False, tag=None):
        output.__init__(self, directory=directory, filename=filename, verbose=verbose, tag=tag)

        self.shorts       = 0
        self.mediums      = 0
        self.longs        = 0
        self.florals      = 0
        self.len_16_to_25 = 0
        self.len_26_to_40 = 0
        self.len_over_40  = 0

    def reset(self):
        self.shorts       = 0
        self.mediums      = 0
        self.longs        = 0
        self.florals      = 0
        self.len_16_to_25 = 0
        self.len_26_to_40 = 0
        self.len_over_40  = 0

    def __str__(self):

        res = "%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f" \
            % ("shorts", self.shorts,"mediums", self.mediums, "longs", self.longs,
                "florals", self.florals, "len_16_to_25",self.len_16_to_25,
                "leng_25_to_40",self.len_26_to_40, "len_over_40",self.len_over_40)
        return res

    def save(self, date=None):
        if self.file is None:
            raise IOError("File is not openned. Use init() method.")

        if date:
            self.file.write("%s\t %s\t %s\t %s\t 0\t %s\t %s\t %s\t %s\n" % (date, self.shorts, self.longs, self.florals, self.mediums, self.len_16_to_25, self.len_26_to_40, self.len_over_40))
        else:
            self.file.write("%s\t %s\t %s\t 0\t %s\t %s\t %s\t %s\n" % (self.shorts, self.longs, self.florals, self.mediums, self.len_16_to_25, self.len_26_to_40, self.len_over_40))


class l_string(output):
    """Defines the output filename to store lstring information"""

    def __init__(self, directory='', filename="l-string", frequency=5., verbose=False, tag=None):
        output.__init__(self, directory=directory, filename=filename, verbose=verbose, frequency=frequency, tag=tag)
        self.filename = filename
    #Added by Han on 12-12-2011
    def build_filename(self, extra=""):
        self.filename = extra + ".dat"

    def save(self, lstring, date):
        self.file.write("%s\tR" % date)

        for i, elt in enumerate(lstring):
            if elt.name=='apex':
                self.file.write("A")
            elif elt.name=='growth_unit':
                self.file.write("G")
            elif elt.name=='metamer':
                if elt[0].observation=='dormant':
                    self.file.write("Id")
                elif elt[0].observation =='large':
                    self.file.write("Il")
                elif elt[0].observation =='medium':
                    self.file.write("Im")
                elif elt[0].observation =='small':
                    self.file.write("Is")
                elif elt[0].observation =='floral':
                    self.file.write("If")
                elif elt[0].observation =='trunk':
                    self.file.write("It")
                elif elt[0].observation =='new_shoot':
                    self.file.write("In")
                else:
                    self.file.write("Ix")
                if elt[0].leaf.state != 'scar':
                        self.file.write("L")
            elif elt.name=='[':
                self.file.write("[")
            elif elt.name==']':
                self.file.write("]")
        self.file.write('\n')
        self.file.flush()

"""
class light_interception(output):
    #Defines the output filename to store light interception information

    def __init__(self,  filename="light-interception", frequency=5., verbose=False, tag=None):
        output.__init__(self, filename=filename, verbose=verbose, frequency=frequency, tag=tag)

    def save(self, lstring, date):
        self.file.write("%s\tR" % date)

        for i, elt in enumerate(lstring):
            if elt[0].leaf.state != 'scar':
                        self.file.write("%s\n" % elt[0].leaf.lg)
        self.file.write('\n')
        self.file.flush()
"""

class sequences(output):
    """

    """
    def __init__(self, directory='', filename="sequences", frequency=5., verbose=False, tag=None):
        output.__init__(self, directory=directory, filename=filename, verbose=verbose, frequency=frequency, tag=tag)

    def save(self, sequence, position):
       for i in range(position - 1,  -1, -1): #up to -1 (c notation so really it's up to 0)
            if i==0:
                self.file.write("%s\n" % sequence[i][1])
            else:
                self.file.write("%s " % sequence[i][1])


header = """# MTG generated by MAppleT 2
#
# Symbols
#   T - tree
#   G - start of a growth unit of a vegetative shoot
#   I - start of a growth unit of an inflorescence
#   M - a metamer
# Features
#   date    - observation date
#   year    - year of creation
#   radius  - radius of an metemer in millimetres
#   length  - length of an metamer in millimetres
#   x, y, z - coordinates, in metres,  of the end of the internode in space

CODE:\tFORM-A
CLASSES:
SYMBOL\tSCALE\tDECOMPOSITION\tINDEXATION\tDEFINITION
$\t0\tFREE\tFREE\tEXPLICIT
T\t1\tLINEAR\tFREE\tEXPLICIT
G\t2\t<-LINEAR\tFREE\tEXPLICIT
I\t2\t<-LINEAR\tFREE\tEXPLICIT
M\t3\tNONE\tFREE\tEXPLICIT

DESCRIPTION:
LEFT\tRIGHT\tRELTYPE\t MAX
G\tG,I\t+\t?
G\tG,I\t<\t1
I\tG,I\t+\t?
I\tG,I\t<\t1
M\tM\t+\t?
M\tM\t<\t1

FEATURES:
NAME\tTYPE
TopDia\tREAL
XX\tREAL
YY\tREAL
ZZ\tREAL
year\tINT
observation\tALPHA
length\tREAL
leaf_state\tALPHA
leaf_area\tREAL
ta_pgl\tREAL
sa_pgl\tREAL
star_pgl\tREAL
unit_id\tINT
branch_id\tINT
lstring_id\tINT
zone\tALPHA
radius\tREAL
fruit\tREAL

MTG:
TOPO\t\t\t\t\t\t\t\t\t\t\tTopDia\tXX\tYY\tZZ\tyear\tobservation\tlength\tleaf_state\tleaf_area\tta_pgl\tsa_pgl\tstar_pgl\tunit_id\tbranch_id\tlstring_id\tzone\tradius\tfruit
"""

#MTG:
#TOPO\t\t\t\t\t\t\t\t\t\t\tTopDia\tXX\tYY\tZZ\tdate\tyear\tobservation\tlength\tleaf_state\tleaf_area\tta_pgl\tsa_pgl\t star_pgl\tunit_id\tbranch_id
#TOPO\t\t\t\t\t\t\t\t\t\t\tTopDia\tXX\tYY\tZZ\tyear\tlength

#% MTG().write_trailing_tabs()


class mtg(output):
    """a simple MTG classes to save output in MTG format."""

    def __init__(self, directory='', filename="", frequency=2., verbose=False, tag=None):
      output.__init__(self, directory=directory, filename=filename, verbose=verbose, frequency=frequency, tag=tag)
      self.columns        = 10;
      self.current_column =  0;
      self.header = header
      self.filename = filename

    #Added by Han on 12-12-2011
    def build_filename(self, extra=""):
        self.filename = extra + ".mtg"

    def write_leading_tabs(self):
        for i in range(0, self.current_column):
            self.file.write('\t')

    def write_trailing_tabs(self):
        res = '\t'* (self.columns - self.current_column)
        self.file.write(res)

    def write_header(self):
        self.file.write(self.header)

    def save(self, lstring, date, trunk_radius):
        """

        :param date: date in format compatible with `datetime.date()`
        """
        year = date.year
        self.write_header()
        self.current_column = 1
        self.file.write("/T1\t")
        self.write_trailing_tabs()
        self.file.write("\t%.4f\t%.4f\t%.4f\t%.4f\t%4.0f\t%.4f\n" % \
            (trunk_radius * 2000.0, 0.0, 0.0, 0.0, 1994, 0.0))

        for i, elt in enumerate(lstring):
            if i!=0:
                #print lstring[i-1].name
                previous = lstring[i-1].name
            else:
                #print 'NONE'
                previous = None
            if  elt.name=='growth_unit' and previous=='branch':
                u = elt[0]
                self.current_column += 1
                if (self.current_column > self.columns):
                    raise ValueError("ERROR: Not enough columns were allocated for the MTG file.\n");

                self.write_leading_tabs()

                if u.inflorescence:
                    self.file.write('+I' + str(u.index))
                else:
                    self.file.write('+G' + str(u.index))
                self.write_trailing_tabs();
                self.file.write("\t\t\t\t\t%4.0f\n" % u.year)
            elif elt.name=='growth_unit':
                u = elt[0]
                self.write_leading_tabs()


                if u.index==1:
                    self.file.write('/')
                else:
                    self.file.write('^<')
                if u.inflorescence:
                    self.file.write('I' + str(u.index))
                else:
                    self.file.write('G' + str(u.index))
                self.write_trailing_tabs();
                if u.index == 1:
                    self.file.write("\t%.4f\t%.4f\t%.4f\t%.4f\t%4.0f\n" % \
                        (trunk_radius * 2000.0, 0.0, 0.0, 0.0, u.year))

                else:
                    self.file.write("\t\t\t\t\t%4.0f\n"  % u.year)
            elif elt.name=='metamer':
                # Modified by Han on 03-05-2011
                m = lstring[i][0]
                #m = elt[0]
                self.write_leading_tabs();
                if m.number==1:
                    self.file.write("^/M%d"  % m.number)
                else:
                    self.file.write("^<M%d" % m.number)
                self.write_trailing_tabs();
                self.file.write("\t%.4f\t%.4f\t%.4f\t%.4f\t%4.0f\t%s\t%.4f\t%s\t%.4f\t%.4f\t%.4f\t%.4f\t%u\t%u\t%u\t%s\t%.4f\t%.4f\n" \
                    % (m.radius * 2000.0, m.position.x, m.position.y, m.position.z, m.year,\
                        m.parent_observation, m.length, m.leaf.state, m.leaf_area,\
                        m.ta_pgl, m.sa_pgl, m.star_pgl,\
                        m.parent_unit_id, m.parent_fbr_id, i,\
                        m.zone, m.radius, m.fruit.mass))
            elif elt.name=='apex' and not previous == 'branch':
                a = elt
                #This assert was filtered by Han on 06=07-2012 because of an
                #assert error after the modification of plastochrons
                #assert self.current_column > 0
                self.current_column-=1




        self.file.close()
        self.file = None




class Data(object):
    """a data class to manage output data given by stocatree.

    an instance of this class allows to father several output structure such as
    :class:`mtg` and :class:`counts` and to keep track of stocatree revision and
    options, which is needed to reproduce results.


    >>> from openalea.plantik.tools.config import ConfigParams
    >>> from openalea.stocatree import get_shared_data
    >>> from openalea.stocatree.output import Data
    >>> options = ConfigParams(get_shared_data('stocatree.ini'))
    >>> data = Data(options=options, revision=None)
    >>> data.counts.init()
    >>> data.shorts = 10
    >>> data.counts.save('1995-10-10')
    >>> data.close_all()

    """
    def __init__(self, options, revision=None, dir="./"):
      self.options = options                        #The options as defined in the .ini file and opend with ConfigParams
      self.revision = revision                      #A number manually generated ?
      self.lstring = None                           #The lstring from lpy ?
      self.verbose = options.general.verbose        #Bool defined in the options, i.e. .ini file
      self.dir = dir# This is to store the results under a designated directory rather than

      #These are output objects added to the Data class, it may be more interesting to be able to add them
      #dynamically. Will require modifications in init and close_all
      self.l_string =l_string(directory=self.dir, tag=options.general.tag, verbose=self.verbose)
      self.counts = counts(directory=self.dir, tag=options.general.tag, verbose=self.verbose)
      self.trunk = trunk(directory=self.dir, tag=options.general.tag, verbose=self.verbose)
      self.sequences = sequences(directory=self.dir, tag=options.general.tag, verbose=self.verbose)
      self.mtg = mtg(directory=self.dir, tag=options.general.tag, verbose=self.verbose)
      #self.light_interception=light_interception(tag=options.general.tag, verbose=self.verbose)
      
      self.time = []
      self.nfruits = []
      self.mass_fruits = []


    def save(self):
        """pickle this data structure

        .. todo:: to be finalised"""
        import pickle
        file = open('data_'+self.options.general.tag+'.dat', 'w')
        #file.write(scdelf.revision + "\n")
        #for x,y in self.options.iteritems():
        #    file.write(str(x) + "\t\t" + str(y)+"\n")
        file.close()

    def close_all(self):
        """close all the attributes of type :class:`~openalea.stocatree.output.output`
        that is `trunk`, `counts`, `sequences`, `mtg` and `l_string`.
        """
        self.trunk.close()
        self.counts.close()
        self.sequences.close()
        self.mtg.close()
        self.l_string.close()
        #self.light_interception.close()

    def init(self):
        """init all the attributes of type :class:`~openalea.stocatree.output.output`
        that is `trunk`, `counts`, `sequences`, `mtg` and `l_string` and write header
        when required.
        """
        #init the sequence
        if self.options.output.sequences:
            self.sequences.init()
            self.sequences.file.write("#save sequences of each apex\n\n1 VARIABLE\n\nVARIABLE 1 : VALUE\n\n")

        # init the l_srting output
        #Filtered by Han on 12-12-2011
        #if self.options.output.l_string:
        #    self.l_string.init()

        """
        # init the light_interception output
        if self.options.output.light_interception:
            self.light_interception.init()
        """

        # init trunk output
        if self.options.output.trunk:
            self.trunk.init()

        # init the shoot counts output
        if self.options.output.counts:
            self.counts.init()
            self.counts.file.write('#shorts\tlongs\tflorals\t0\tmediums\tlen_16_to_25\tlen_26_to_40\tlen_over_40\tfruits\n')


