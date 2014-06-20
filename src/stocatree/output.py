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
from os.path import join


class output(object):
    """A base class to manage outputs in stocatree.

    This base class allows to define a filename given a basename and a tag
    and then to open/close this file easily.

    It also defines the frequency and period at which data has to be saved.

    Given a frequency, the period is computed as 365./frequency.

    This class also stored the time elapsed since the beginning.

    :param filename: a valid basename (e.g. 'output' in output.txt)
    :param frequency: a frequency to save the data
    :param tag: a tag for the filename


    """
    def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=1., filename=None, ext='.csv'):
      self.basename = filename
      self.ext = ext
      self.init_date = init_date
      self.file = None

      self.frequency = frequency
      self.elapsed = datetime.timedelta(0)
      #by product
      self.period = 365.0 / self.frequency


    def build_filename(self, directory='', tag=None):
      """
      create the filename given an optional tag suffix that is used before the extension
      """
      filename = self.basename
      if tag:
        filename += '_' + tag
      filename += self.ext

      self.filename = join(directory, filename)

    def openfile(self):
      """
      open the file object
      ..warning: `build_filename` must be called prior to `openfile`
      """
      if self.file == None or self.file.closed:
        print 'opening file %s' % self.filename
        self.file = open(self.filename, 'a')
      else:
        print 'File already openned !! Close it first.'

    def close(self):
      """close the file object"""
      if self.file:
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

class counts(output):
  """
  Record the counting of multiple variables evolving during tree development
  """

  def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="counts", ext='.csv'):
    output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)

    self.metamers     = 0 # number of metamers
    self.gus          = 0 # number of growing units
    self.leaves       = 0 # number o leaves
    self.tla          = 0 # Total Leaf Area
    self.fruits       = 0 # number of fruits
    self.fruitdw      = 0 # Total fruit Dry Weight

  def openfile(self):
    output.openfile(self)
    self.file.write('Date, SimuDay, Metamers, GUs, Leaves, TLA, Fruits, Fruit DW\n')

  def update(self, metamer):
    self.metamers += 1
  
    #updating fruit data
    if metamer.fruit.state == 'fruit':
      self.fruits += 1
      self.fruitdw += metamer.fruit.mass

    #updating leaf data
    if metamer.leaf.state == 'growing':
      self.leaves += 1
      self.tla += metamer.leaf.area

  def display(self):
    return ['metamers', 'leaves', 'tla', 'fruits', 'fruitdw']

  def reset(self):
    self.metamers     = 0 # number of metamers
    self.gus          = 0 # number of growing units
    self.leaves       = 0 # number of leaves
    self.tla          = 0 # Total Leaf Area
    self.fruits       = 0 # number of fruits
    self.fruitdw      = 0 # Total fruit Dry Weight

  def save(self, date):
    if self.file is None:
      raise IOError("File is not openned. Use openfile() method.")
     
    self.file.write("{date}, {days}, {metamers}, {gus}, {leaves}, {tla}, {fruits}, {fruitdw}\n".format(date=date, days=(date-self.init_date).days, metamers=self.metamers, gus=self.gus, leaves=self.leaves, tla=self.tla, fruits=self.fruits, fruitdw=self.fruitdw))

  def __str__(self):
    res = "%20s=%10f\t%20s=%10f\n%20s=%10f\t%20s=%10f\n%20s=%10f\t%20s=%10f\n" \
        % ("Metamers: ", self.metamers, "GUs: ", self.gus, "Leaves: ", self.leaves,
            "TLA: ", self.tla, "Fruits: ",self.fruits, "Fruits DW: ",self.fruitdw)
    return res



class shoots(output):
  """
  Record the shoot demography per length type
  """

  def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="shoots", ext='.csv'):
    output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)

    #self.file.write('#shorts\tlongs\tflorals\t0\tmediums\tlen_16_to_25\tlen_26_to_40\tlen_over_40\tfruits\n')

    self.shorts       = 0
    self.mediums      = 0
    self.longs        = 0
    self.florals      = 0
    self.len_16_to_25 = 0
    self.len_26_to_40 = 0
    self.len_over_40  = 0

  def openfile(self):
    output.openfile(self)
    self.file.write('Date, Florals, Shorts, Mediums, All_Longs, Longs_16_to_25, Longs_26_to_40, Longs_over_40\n')


  def reset(self):
    self.shorts       = 0
    self.mediums      = 0
    self.longs        = 0
    self.florals      = 0
    self.len_16_to_25 = 0
    self.len_26_to_40 = 0
    self.len_over_40  = 0

  def display(self):
    return ['shorts', 'mediums', 'longs', 'florals']

  def __str__(self):
    res = "%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f\n%20s=%10f" \
        % ("shorts", self.shorts,"mediums", self.mediums, "longs", self.longs,
            "florals", self.florals, "len_16_to_25",self.len_16_to_25,
            "leng_25_to_40",self.len_26_to_40, "len_over_40",self.len_over_40)
    return res

  def save(self, date):
    if self.file is None:
      raise IOError("File is not openned. Use openfile() method.")
     
    self.file.write("{date}, {florals}, {shorts}, {mediums}, {longs}, {longshort}, {longmedium}, {longlong}\n".format(date=date, florals=self.florals, shorts=self.shorts, mediums=self.mediums, longs=self.longs, longshort=self.len_16_to_25, longmedium=self.len_26_to_40, longlong=self.len_over_40))


class sequences(output):
  """
  Store each generated sequence during the simulation
  """
  def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="sequences", ext='.seq'):
    output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)

  def openfile(self):
    output.openfile(self)
    self.file.write("#save sequences of each apex\n\n1 VARIABLE\n\nVARIABLE 1 : VALUE\n\n")
  
  def save(self, sequence, position):
    for i in range(position - 1,  -1, -1): #up to -1 (c notation so really it's up to 0)
      if i==0:
        self.file.write("%s\n" % sequence[i][1])
      else:
        self.file.write("%s " % sequence[i][1])


class trunk(output):
  """
  Defines the output filename to store trunk information
  """

  def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="trunk", ext='.csv'):
    output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)

    self.trunk_radius = 0
    self.trunk_area = 0

  def openfile(self):
    output.openfile(self)
    self.file.write('Date, SimuDay, Trunk radius, Trunk cross sectional area\n')

  def save(self, date, trunk_radius, trunk_cross_sectional_area):
    self.trunk_radius = trunk_radius
    self.trunk_area = trunk_cross_sectional_area
    self.file.write("{date}, {days}, {radius}, {section_area}\n".format(date=date, days=(date-self.init_date).days, radius=trunk_radius, section_area=trunk_cross_sectional_area))

  def display(self):
    return ['trunk_radius', 'trunk_area']

class l_string(output):
    """Defines the output filename to store lstring information"""

    def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="l-string", ext='.lsys'):
      output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)
      self.filename = filename

    #Added by Han on 12-12-2011
    #def build_filename(self, extra=""):
    #    self.filename = extra + ".dat"

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

  def __init__(self, init_date=datetime.datetime(1994,1,1), frequency=365., filename="trunk", ext='.mtg'):
    output.__init__(self, init_date=init_date, frequency=frequency, filename=filename, ext=ext)

    self.columns        = 10;
    self.current_column =  0;
    self.header = header
    self.filename = filename


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

    an instance of this class allows to gather several output structure such as
    :class:`mtg` and :class:`shoots` and to keep track of stocatree revision and
    options, which is needed to reproduce results.

    #wrong example needs update
    >>> from openalea.plantik.tools.config import ConfigParams
    >>> from openalea.stocatree import get_shared_data
    >>> from openalea.stocatree.output import Data
    >>> options = ConfigParams(get_shared_data('stocatree.ini'))
    >>> data = Data(options=options)
    >>> data.shoots.openfile()
    >>> data.shoots = 10
    >>> data.shoots.save('1995-10-10')
    >>> data.close_all()

    """
    def __init__(self, options, init_date, directory="./"):
      self.options = options                        #The options as defined in the .ini file and opend with ConfigParams
      self.init_date = init_date                    #The starting date of recording outputs
      self.lstring = None                           #The lstring from lpy ?
      self.directory = directory# This is to store the results under a designated directory rather than

      #These are output objects added to the Data class, it may be more interesting to be able to add them
      #dynamically. Will require modifications in openfile and close_all

      if self.options.output.shoots:
        self.shoots = shoots(init_date=self.init_date)

      if self.options.output.sequences:
        self.sequences = sequences(init_date=self.init_date)

      if self.options.output.trunk:
        self.trunk = trunk(init_date=self.init_date)

      if self.options.output.counts:
        self.counts = counts(init_date=self.init_date)

      if self.options.output.mtg :
        self.mtg = mtg(init_date=self.init_date)

      #self.l_string =l_string(directory=self.directory, tag=options.general.tag, verbose=self.verbose)
      #self.light_interception=light_interception(tag=options.general.tag, verbose=self.verbose)
      
      #self.time = []
      #self.nfruits = []
      #self.mass_fruits = []

    def open_all(self, simu_id):
      """
      open all the files of :class:`~openalea.stocatree.output.output`
      i.e.: `shoots`, `sequences`, `trunk` and `counts`.
      """

      # init the shoots output
      if self.options.output.shoots:
        self.shoots.build_filename(directory=self.directory, tag="{0}_{1}".format(self.options.general.tag, simu_id))
        self.shoots.openfile()

      #init the sequence
      if self.options.output.sequences:
        self.sequences.build_filename(directory=self.directory, tag="{0}_{1}".format(self.options.general.tag, simu_id))
        self.sequences.openfile()

      # init trunk output
      if self.options.output.trunk:
        self.trunk.build_filename(directory=self.directory, tag="{0}_{1}".format(self.options.general.tag, simu_id))
        self.trunk.openfile()

      # init counts output
      if self.options.output.counts:
        self.counts.build_filename(directory=self.directory, tag="{0}_{1}".format(self.options.general.tag, simu_id))
        self.counts.openfile()

      # init the l_srting output
      #Filtered by Han on 12-12-2011
      #if self.options.output.l_string:
      #    self.l_string.openfile()




    def save(self):
        """pickle this data structure

        .. todo:: to be finalised"""
        #import pickle
        #file = open('data_'+self.options.general.tag+'.dat', 'w')
        #file.write(scdelf.revision + "\n")
        #for x,y in self.options.iteritems():
        #    file.write(str(x) + "\t\t" + str(y)+"\n")
        #file.close()
        print("Data.save() is not implemented")

    def close_all(self):
      """
      Close all the attributes of type :class:`~openalea.stocatree.output.output`
      that is `shoots`, `sequences`, `mtg`.
      """
      if self.options.output.shoots:
        self.shoots.close()
      if self.options.output.sequences:
        self.sequences.close()
      if self.options.output.trunk:
        self.trunk.close()
      if self.options.output.counts:
        self.counts.close()

      if self.options.output.mtg :
        self.mtg.close()
        #self.trunk.close()
        #self.light_interception.close()

