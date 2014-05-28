#!/usr/bin/python
#MAppleTParameters

import sys
import numpy as np


from openalea.vpltk.qt import *
import openalea.lpy as lpy
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree import get_shared_data

#from PyQt4 import QtCore, QtGui

class myCheckBox(QtGui.QCheckBox):
  def __init__(self, parent, section, variable, value):
    
    QtGui.QCheckBox.__init__(self, variable, parent)
    self.section = section
    self.variable = variable
    self.setChecked(value)
    self.connect(self, QtCore.SIGNAL('toggled(bool)'), self.update)

  def update(self, checked):
    self.emit(QtCore.SIGNAL("refresh"), self.section, self.variable, checked)
    
class myIntSpinBox(QtGui.QWidget):
  def __init__(self, parent, section, variable, value):

    QtGui.QWidget.__init__(self, parent)
    self.section = section
    self.variable = variable
    layout = QtGui.QHBoxLayout()
    layout.addWidget(QtGui.QLabel('{:<50}'.format(variable)))
    spinbox = QtGui.QSpinBox()
    spinbox.setRange(-sys.maxint/100, sys.maxint/100)
    #spinbox.setRange(-1000.*value, 1000.*value)
    spinbox.setValue(value)
    layout.addWidget(spinbox)
    self.setLayout(layout)
    self.connect(spinbox, QtCore.SIGNAL("valueChanged(int)"), self.update)
    
  def update(self, value):
    self.emit(QtCore.SIGNAL("refresh"), self.section, self.variable, value)
    
class myFloatSpinBox(QtGui.QWidget):
  def __init__(self, parent, section, variable, value):

    QtGui.QWidget.__init__(self, parent)
    self.section = section
    self.variable = variable
    layout = QtGui.QHBoxLayout()
    layout.addWidget(QtGui.QLabel('{:<50}'.format(variable)))
    spinbox = QtGui.QDoubleSpinBox()
    spinbox.setRange(-sys.maxint, sys.maxint)
    deci = len(str(value).split('.')[1])
    spinbox.setDecimals(deci)
    spinbox.setSingleStep(10**-deci)
    spinbox.setValue(value)
    layout.addWidget(spinbox)
    self.setLayout(layout)
    self.connect(spinbox, QtCore.SIGNAL("valueChanged(double)"), self.update)

  def update(self, value):
    self.emit(QtCore.SIGNAL("refresh"), self.section, self.variable, value)
    

class myComboBox(QtGui.QWidget):
  def __init__(self, parent, section, variable, value):

    QtGui.QWidget.__init__(self, parent)
    self.section = section
    self.variable = variable
    layout = QtGui.QHBoxLayout()
    layout.addWidget(QtGui.QLabel('{:<50}'.format(variable)))
    combox = QtGui.QComboBox(self)
    combox.addItems(value)
    layout.addWidget(combox)
    self.setLayout(layout)
    self.connect(combox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.update)

  def update(self, value):
    self.emit(QtCore.SIGNAL("refresh"), self.section, self.variable, str(value))


class myLineEdit(QtGui.QWidget):
  def __init__(self, parent, section, variable, value):

    QtGui.QWidget.__init__(self, parent)
    self.section = section
    self.variable = variable
    layout = QtGui.QHBoxLayout()
    layout.addWidget(QtGui.QLabel('{:<50}'.format(variable)))
    line = QtGui.QLineEdit()
    line.setText(value)
    layout.addWidget(line)
    self.setLayout(layout)
    self.connect(line, QtCore.SIGNAL("textChanged(QString)"), self.update)


  def update(self, value):
    self.emit(QtCore.SIGNAL("refresh"), self.section, self.variable, str(value))

class MyWindow(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)

    self.confp=None
    self._loadIni_()
   
    #Puts the settings widgets into tabs
    self.centerTabs = QtGui.QTabWidget(self)

    self._genSectionTabs_()
   
    self.setCentralWidget(self.centerTabs)
    
    self.setWindowTitle(' MAppleT Parameter Editor')

    self.createActions()
    self.createMenus()
    self.resize(800,600)

    self.lsys = lpy.Lsystem(self.confp.general.filename, {"options":self.confp})

  def myPostDraw(self):
    QtCore.QCoreApplication.processEvents()

  def createActions(self):
    self.openAction = QtGui.QAction('&Open...', self)
    self.openAction.setShortcut("Ctrl+O")
    self.openAction.setStatusTip("Load settings from an .ini file.")
    self.connect(self.openAction, QtCore.SIGNAL('triggered()'), self.loadSettings)
        
    self.saveAsAction = QtGui.QAction('Save As...', self)
    #self.saveAsAction.setShortcut("Ctrl+Alt+S")
    self.saveAsAction.setStatusTip("Save these settings as a file.")
    self.connect(self.saveAsAction, QtCore.SIGNAL('triggered()'), self.saveAs)

    self.quitAction = QtGui.QAction('&Quit', self)
    self.quitAction.setShortcut("Ctrl+Q")
    self.quitAction.setStatusTip("Quit the application")
    self.connect(self.quitAction, QtCore.SIGNAL("triggered()"), self.close)

    self.goAction = QtGui.QAction('&Go', self)
    self.goAction.setStatusTip("Start the model with the current settings.")
    self.connect(self.goAction, QtCore.SIGNAL('triggered()'), self.go)
        
    self.helpAction = QtGui.QAction('&Help', self)
    self.connect(self.helpAction, QtCore.SIGNAL('triggered()'), self.help)


  def createMenus(self):
    fileMenu = self.menuBar().addMenu('&File')
    fileMenu.addAction(self.openAction)
    fileMenu.addAction(self.saveAsAction)
    fileMenu.addAction(self.quitAction)
    
    self.menuBar().addAction(self.goAction)
    self.menuBar().addAction(self.helpAction)

  def loadSettings(self):
    self._loadIni_()
    self.centerTabs = QtGui.QTabWidget(self)
    self._genSectionTabs_()
    self.setCentralWidget(self.centerTabs)
    
  def saveAs(self):
      settingsFileName = str(QtGui.QFileDialog.getSaveFileName(self, '', '', "MS ini file(*.ini)"))
      self.confp.save(settingsFileName) 

  def go(self):

    self.lsys = lpy.Lsystem(self.confp.general.filename, {"options":self.confp, 'PostDraw':self.myPostDraw})
    self.lsys.animate()    

  #May provide general and/or tab specific help later
  def help(self):
    QtGui.QMessageBox.information(self, 'Help', 'Currently there is no help. You are doomed.')
    #QtGui.QWhatsThis.enterWhatsThisMode()

  def updateConf(self,section, var, val):
    self.confp.__dict__[section].__dict__[var] = val
    self.confp.config.set(section, var, val)
    self.lsys.context()['options'].__dict__[section].__dict__[var] = val
    #print "updated section {0} variable {1} with value {2}".format(section, var, val)


  def _loadIni_(self):
    #Open a file browser to choose the ini file to build the interface 
    #iniFilePath = QtGui.QFileDialog.getOpenFileName(self, QtCore.QString(), QtCore.QString(), 'INI (*.ini)')
    iniFilePath = QtGui.QFileDialog.getOpenFileName(self, '', '', 'INI (*.ini)')
      
    if iniFilePath != '':
      self.confp = ConfigParams(str(iniFilePath))

  def _genSectionTabs_(self):
    for sec in self.confp.config.sections():
      newTab = self._fillTab_(sec)
      self.centerTabs.addTab(newTab, sec)

  def _fillTab_(self, section):
    newTab = QtGui.QWidget(parent=self)
    layout = QtGui.QVBoxLayout()
    for var in self.confp.config.options(section):
      try: # int
        val = self.confp.config.getint(section, var)
        spinBox = myIntSpinBox(self, section, var, val)
        layout.addWidget(spinBox)
        self.connect(spinBox, QtCore.SIGNAL("refresh"), self.updateConf)
      except ValueError:
        try: #float
          val = self.confp.config.getfloat(section, var)
          spinBox = myFloatSpinBox(self, section, var, val)
          layout.addWidget(spinBox)
          self.connect(spinBox, QtCore.SIGNAL("refresh"), self.updateConf)
        except: #string
          val = self.confp.config.get(section, var)
          
          if val in ['True', 'Yes', 'true', 'yes']:
            checkBox = myCheckBox(self, section, var, True)
            layout.addWidget(checkBox)
            self.connect(checkBox, QtCore.SIGNAL("refresh"), self.updateConf)
          elif val in ['False', 'false', 'no', 'No']:
            checkBox = myCheckBox(self, section, var, False)
            layout.addWidget(checkBox)
            self.connect(checkBox, QtCore.SIGNAL("refresh"), self.updateConf)
          elif val[0] == '[':
            val = val.replace('[', '')
            val = val.replace(']', '')
            choices = [ v.strip() for v in val.split(',')]
            comboBox = myComboBox(self, section, var, choices)
            layout.addWidget(comboBox)
            self.connect(comboBox, QtCore.SIGNAL("refresh"), self.updateConf)
          else:
            #val = self.confp.config.get(section, var)
            lineEdit = myLineEdit(self, section, var, val)
            layout.addWidget(lineEdit)
            self.connect(lineEdit, QtCore.SIGNAL("refresh"), self.updateConf)

    
    newTab.setLayout(layout)
    return newTab  


#creates and shows the qt window

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
