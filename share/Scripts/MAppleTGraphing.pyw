#MAppleT Graphing
import sys, os, os.path, traceback, gc

from PyQt4 import QtCore, QtGui
import matplotlib as mpl
mpl.use('Qt4Agg')
import matplotlib.pyplot as plt
import numpy

import graphFiles


# # # # # # # # # #
# My Settings Tab #
# # # # # # # # # #
class MySettingsTab(QtGui.QWidget):
    def __init__(self, parent=None, fileName=''):
        QtGui.QWidget.__init__(self, parent)
        
        self.fileName = fileName
        
        self.widget = QtGui.QWidget(self)
        self.headers = self.getHeaderDict()
        
        
        self.boxLayout = QtGui.QVBoxLayout(self)
        
        self.boxLayout.addWidget(self.createHeadersListWidgets(), 1)
        self.boxLayout.addWidget(self.createGeneralOptions())
        self.boxLayout.addWidget(self.createLineStyleGroup())
        self.boxLayout.addWidget(self.createFilteringGroup(), 1)
        self.boxLayout.addWidget(self.createDynamicGroup())
        self.boxLayout.addWidget(self.createGraphControlGroup())
        
        
        #These functions are called to set the widgets into the correct state
        # self.shootSegmentEnable()
        #self.dynamicToggled()
        self.plotButtonEnable()
        
        
        self.setLayout(self.boxLayout)
    
    # # # # # # # # # #
    # Get Header Dict #
    # # # # # # # # # #
    def getHeaderDict(self):
        dict = {}
        
        try:
            file = open(self.fileName, 'r')
        except EnvironmentError as e:
            QtGui.QMessageBox.critical(self, 'File Error', 'An error occured while opening a file.\n' +
                                                            str(e) + '\n' + traceback.format_exc())
        else:
            #Gets the header list from the first line of the file
            #Puts them in a dict with the name as the key and the column number as the value
            list = file.readline().split(',')
            for key in list:
                dict[key.strip()] = list.index(key)
            return dict
        finally:
            file.close()
    
    
    # # # # # # # # # #
    # List of Headers #
    # # # # # # # # # #
    def createHeadersListWidgets(self):
        groupBox           = QtGui.QGroupBox  ('Variables', self)
        hBoxLayout         = QtGui.QHBoxLayout()
        arrowsVBoxLayout   = QtGui.QVBoxLayout()
        headersVBoxLayout  = QtGui.QVBoxLayout()
        selectedVBoxLayout = QtGui.QVBoxLayout()
        
        
        self.headersListWidget = QtGui.QListWidget(self)
        self.headersListWidget.setSortingEnabled(True)
        self.headersListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.selectedListWidget = QtGui.QListWidget(self)
        self.selectedListWidget.setSortingEnabled(True)
        self.selectedListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.leftArrowPushButton  = QtGui.QPushButton('<' , self)
        self.leftAllPushButton    = QtGui.QPushButton('<<', self)
        self.rightAllPushButton   = QtGui.QPushButton('>>', self)
        self.rightArrowPushButton = QtGui.QPushButton('>' , self)
        
        self.leftArrowPushButton.setMaximumWidth(25)
        self.leftAllPushButton.setMaximumWidth(25)
        self.rightAllPushButton.setMaximumWidth(25)
        self.rightArrowPushButton.setMaximumWidth(25)
        
        
        # Add the headers to the list widget
        self.headersListWidget.addItems(self.headers.keys())
        
        
        #Connect SIGNALs
        self.connect(self.leftArrowPushButton , QtCore.SIGNAL('clicked()'), self.leftArrowClicked)
        self.connect(self.leftAllPushButton   , QtCore.SIGNAL('clicked()'), self.leftAllClicked)
        self.connect(self.rightAllPushButton  , QtCore.SIGNAL('clicked()'), self.rightAllClicked)
        self.connect(self.rightArrowPushButton, QtCore.SIGNAL('clicked()'), self.rightArrowClicked)
        
        
        #Layout design
        arrowsVBoxLayout.addWidget(self.leftArrowPushButton)
        arrowsVBoxLayout.addWidget(self.leftAllPushButton)
        arrowsVBoxLayout.addWidget(self.rightAllPushButton)
        arrowsVBoxLayout.addWidget(self.rightArrowPushButton)
        
        selectedVBoxLayout.addWidget(QtGui.QLabel('Selected Headers'))
        selectedVBoxLayout.addWidget(self.selectedListWidget)
        
        headersVBoxLayout.addWidget(QtGui.QLabel('Unselected Headers'))
        headersVBoxLayout.addWidget(self.headersListWidget)
        
        
        hBoxLayout.addLayout(selectedVBoxLayout)
        hBoxLayout.addLayout(arrowsVBoxLayout)
        hBoxLayout.addLayout(headersVBoxLayout)
        
        
        groupBox.setLayout(hBoxLayout)
        
        return groupBox
    
    def getSelectedHeaders(self):
        headerdict = {}
        for i in range(self.selectedListWidget.count()):
            headerdict[str(self.selectedListWidget.item(i).text())] = self.headers[str(self.selectedListWidget.item(i).text())]
        headerdict[str(self.xaxisComboBox.currentText())] = self.headers[str(self.xaxisComboBox.currentText())]
        
        return headerdict
    
    def leftArrowClicked(self):
        for item in self.headersListWidget.selectedItems():
            self.selectedListWidget.addItem(item.text())
            self.headersListWidget.takeItem(self.headersListWidget.indexFromItem(item).row())
    
    def leftAllClicked(self):
        self.headersListWidget.clear()
        self.selectedListWidget.clear()
        self.selectedListWidget.addItems(self.headers.keys())
    
    def rightAllClicked(self):
        self.selectedListWidget.clear()
        self.headersListWidget.clear()
        self.headersListWidget.addItems(self.headers.keys())
    
    def rightArrowClicked(self):
        for item in self.selectedListWidget.selectedItems():
            self.headersListWidget.addItem(item.text())
            self.selectedListWidget.takeItem(self.selectedListWidget.indexFromItem(item).row())
    
    
    # # # # # # # # # #
    # General Options #
    # # # # # # # # # #
    def createGeneralOptions(self):
        groupBox = QtGui.QGroupBox("General Options", self)
        hBoxLayout = QtGui.QHBoxLayout(groupBox)
        
        
        self.xaxisComboBox = QtGui.QComboBox(self)
        tempList = self.headers.keys()
        tempList.sort()
        tempList.insert(0, "--X-Axis--")
        self.xaxisComboBox.addItems(tempList)
        if 'HourIndex' in tempList:
            self.xaxisComboBox.setCurrentIndex(self.xaxisComboBox.findText('HourIndex'))
        
        self.columnSpinBox = QtGui.QSpinBox(self)
        self.columnSpinBox.setRange(1, 128)
        self.columnSpinBox.setSuffix("  Column(s)")
        
        self.singleGraphCheckBox = QtGui.QCheckBox("Single Graph", self)
        
        self.showLegendCheckBox = QtGui.QCheckBox("Show Legend", self)
        self.showLegendCheckBox.setChecked(True)
        
        self.figureTitleLineEdit = QtGui.QLineEdit(self)
        
        #connect SIGNALs
        self.connect(self.xaxisComboBox, QtCore.SIGNAL('activated(QString)'), self.plotButtonEnable)
        
        
        #Layout design
        axesVBoxLayout = QtGui.QVBoxLayout()
        axesVBoxLayout.addWidget(self.xaxisComboBox)
        axesVBoxLayout.addWidget(self.columnSpinBox)
        hBoxLayout.addLayout(axesVBoxLayout)
        
        checkVBoxLayout = QtGui.QVBoxLayout()
        checkVBoxLayout.addWidget(self.singleGraphCheckBox)
        checkVBoxLayout.addWidget(self.showLegendCheckBox)
        hBoxLayout.addLayout(checkVBoxLayout)
        
        figTitleVBoxLayout = QtGui.QVBoxLayout()
        figTitleVBoxLayout.addWidget(QtGui.QLabel('Figure Title'))
        figTitleVBoxLayout.addWidget(self.figureTitleLineEdit)
        
        hBoxLayout.addLayout(figTitleVBoxLayout)
        
        groupBox.setLayout(hBoxLayout)
        
        return groupBox
    
    def get_fig_title(self):
        return str(self.figureTitleLineEdit.text())
    
    # # # # # # # # # # #
    # Line Style Group  #
    # # # # # # # # # # #
    def createLineStyleGroup(self):
        lineStyleGroupBox = QtGui.QGroupBox('Line Style Options', self)
        hBoxLayout = QtGui.QHBoxLayout(lineStyleGroupBox)
        
        lineStyleVBoxLayout = QtGui.QVBoxLayout()
        lineStyleVBoxLayout.addWidget(QtGui.QLabel('Line Type:'))
        self.lineTypeComboBox = QtGui.QComboBox(self)
        lineStyleVBoxLayout.addWidget(self.lineTypeComboBox)
        #lineStyleVBoxLayout.addStretch(1)
        
        for style in plt.Line2D.lineStyles.values():
            style = style.replace('_draw_', '')
            if self.lineTypeComboBox.findText(style) == -1:
                self.lineTypeComboBox.addItem(style)
        tmp = self.lineTypeComboBox.findText('solid')
        if tmp != -1:
            self.lineTypeComboBox.setCurrentIndex(tmp)
        
        
        #lineWidthVBoxLayout = QtGui.QVBoxLayout()
        #lineWidthVBoxLayout.addWidget(QtGui.QLabel('Line Width:'))
        lineStyleVBoxLayout.addWidget(QtGui.QLabel('Line Width:'))
        self.lineWidthSpinBox = QtGui.QSpinBox(self)
        lineStyleVBoxLayout.addWidget(self.lineWidthSpinBox)
        #lineWidthVBoxLayout.addWidget(self.lineWidthSpinBox)
        #lineWidthVBoxLayout.addStretch(1)
        self.lineWidthSpinBox.setSuffix(' pixel(s)')
        self.lineWidthSpinBox.setMinimum(0)
        self.lineWidthSpinBox.setValue(1)
        
        self.markerGroupBox = QtGui.QGroupBox('Use Markers', self)
        self.markerGroupBox.setCheckable(True)
        self.markerGroupBox.setChecked(False)
        markerVBoxLayout = QtGui.QVBoxLayout()
        self.markerGroupBox.setLayout(markerVBoxLayout)
        
        markerVBoxLayout.addWidget(QtGui.QLabel('Marker Size:'))
        self.markerSizeSpinBox = QtGui.QSpinBox(self.markerGroupBox)
        markerVBoxLayout.addWidget(self.markerSizeSpinBox)
        self.markerSizeSpinBox.setMinimum(1)
        self.markerSizeSpinBox.setValue(5)
        
        
        #Layout Design
        hBoxLayout.addLayout(lineStyleVBoxLayout)
        #hBoxLayout.addLayout(lineWidthVBoxLayout)
        hBoxLayout.addWidget(self.markerGroupBox)
        
        lineStyleGroupBox.setLayout(hBoxLayout)
        
        return lineStyleGroupBox
    
    def get_linestyle(self):
        lineDict = {}
        lineDict['linewidth'] = self.lineWidthSpinBox.value()
        lineDict['linestyle'] = '_draw_' + str(self.lineTypeComboBox.currentText())
        lineDict['marker'] = self.markerGroupBox.isChecked()
        if lineDict['marker']:
            lineDict['markersize'] = self.markerSizeSpinBox.value()
        else:
            lineDict['markersize'] = None
        
        return lineDict
    
    # # # # # # # # # #
    # Filtering Group #
    # # # # # # # # # #
    def createFilteringGroup(self):
        self.filteringGroupBox = QtGui.QGroupBox('Use additional filtering', self)
        self.filteringGroupBox.setCheckable(True)
        self.filteringGroupBox.setChecked(False)
        
        self.filterHBoxLayout = QtGui.QHBoxLayout(self.filteringGroupBox)
        
        self.sortedHeadersList = self.headers.keys()
        self.sortedHeadersList.sort()
        
        self.dataFileSize = os.path.getsize(self.fileName)
        
        self.filterDir = 'Filtered Datafiles'
        try:
            os.mkdir(self.filterDir)
        except OSError as e:
            if not os.path.isdir(self.filterDir):
                raise e
        
        self.filterList = []
        
        self.addFilterPushButton = QtGui.QPushButton('Add Filter')
        self.addFilterPushButton.setDisabled(True)
        
        self.removeFilterPushButton = QtGui.QPushButton('Remove Filter')
        self.removeFilterPushButton.setDisabled(True)
        
        self.updateFilterPushButton = QtGui.QPushButton('Update')
        self.updateFilterPushButton.setDisabled(True)
        
        self.filterIntoFilePushButton = QtGui.QPushButton('Filter into File')
        self.filterIntoFilePushButton.setDisabled(True)
        
        
        #connect SIGNALs
        self.connect(self.filteringGroupBox, QtCore.SIGNAL('toggled(bool)'), self.filterBoxChanged)
        
        self.connect(self.addFilterPushButton, QtCore.SIGNAL('clicked()'), self.createAdditionalFilterChoice)
        self.connect(self.removeFilterPushButton, QtCore.SIGNAL('clicked()'), self.removeLastFilter)
        self.connect(self.updateFilterPushButton, QtCore.SIGNAL('clicked()'), self.filterComboBoxActivated)
        self.connect(self.filterIntoFilePushButton, QtCore.SIGNAL('clicked()'), self.createFilteredFile)
        
        
        #design Layouts
        buttonVBoxLayout = QtGui.QVBoxLayout(self.filteringGroupBox)
        buttonVBoxLayout.addWidget(self.addFilterPushButton)
        buttonVBoxLayout.addWidget(self.removeFilterPushButton)
        buttonVBoxLayout.addWidget(self.updateFilterPushButton)
        buttonVBoxLayout.addWidget(self.filterIntoFilePushButton)
        
        self.filterHBoxLayout.addLayout(buttonVBoxLayout)
        self.createAdditionalFilterChoice()
        self.filterBoxChanged(False)
        
        self.filteringGroupBox.setLayout(self.filterHBoxLayout)
        
        return self.filteringGroupBox
    
    def createAdditionalFilterChoice(self):
        if len(self.filterList) > 0:
            widgetList = self.filterList[len(self.filterList) - 1]
            
            if len(widgetList[1].selectedItems()) > 1:
                widgetList[1].setCurrentItem(None)
            
            widgetList[1].setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        
        self.filterList.append([])
        length = len(self.filterList) - 1
        
        self.filterList[length].append(QtGui.QComboBox(self))
        self.filterList[length][0].addItems(['--Filter--'] + self.sortedHeadersList)
        #connect SIGNAL
        #self.connect(self.filterList[length][0], QtCore.SIGNAL('activated(QString)'), self.filterComboBoxActivated)
        
        self.filterList[length].append(QtGui.QListWidget(self))
        self.filterList[length][1].setDisabled(True)
        self.filterList[length][1].setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        #design Layouts
        layout = QtGui.QVBoxLayout()
        for widget in self.filterList[length]:
            layout.addWidget(widget)
        
        
        self.filterList[length].append(str(self.filterList[length][0].currentText()))
        self.filterList[length].append(layout)
        
        self.filterHBoxLayout.addLayout(self.filterList[length][len(self.filterList[length])-1])
        
        self.filterBoxChanged()
    
    def removeLastFilter(self):
        widgetList = self.filterList[len(self.filterList) - 1]
        
        for widget in widgetList:
            try:
                self.filterHBoxLayout.removeWidget(widget)
                widget.hide()
                widget.destroy()
            except TypeError as e:
                try:
                    self.filterHBoxLayout.removeItem(widget)
                except TypeError as e2:
                    pass #print 'Info: Non-Qt type could not be removed.\n' + str(type(widget))
        
        self.filterList.remove(widgetList)
        
        widgetList = self.filterList[len(self.filterList) - 1]
        
        widgetList[1].setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        
        self.filterBoxChanged()
    
    def filterBoxChanged(self, active=True):
        self.addFilterPushButton.setEnabled(active)
        self.updateFilterPushButton.setEnabled(active)
        self.filterIntoFilePushButton.setEnabled(active)
        
        self.removeFilterPushButton.setEnabled(active and len(self.filterList) >= 2)
        
        filterUnused = False
        for widgetList in self.filterList:
            for widget in widgetList:
                try:
                    widget.setEnabled(active and not filterUnused)
                except AttributeError as e:
                    pass
            
            if str(widgetList[0].currentText()) == '--Filter--':
                filterUnused = True
    
    def filterComboBoxActivated(self):
        for widgetList in self.filterList:
            if str(widgetList[0].currentText()) != widgetList[2] or widgetList is self.filterList[-1]:
                widgetList[1].clear()
                widgetList[2] = str(widgetList[0].currentText())
                if str(widgetList[0].currentText()) != '--Filter--':
                    filters = self.getFilteredItems(str(widgetList[0].currentText()))
                    if filters != -1:
                        widgetList[1].addItems(filters)
                else:
                    break
        
        self.filterBoxChanged()
    
    def getFilteredItems(self, header):
        #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
        self.parentWidget().parentWidget().parentWidget().busy('start')
        
        singleCol = [self.headers.get(header)]
        
        bestfilter = self.getPreviousFilter(self.getFilteringChoice())
        
        if len(bestfilter) == 1:
            dataFile = self.makeFilteredFile(self.getFilteringChoice(), bestfilter[0])
            try:
                sortedArray = numpy.loadtxt(dataFile, delimiter=',', skiprows=1, usecols=singleCol)
            except IOError as e:
                QtGui.QMessageBox.critical(self, 'File Error', 'The file may not have data.\n' +
                                                                repr(e) + '\n' + traceback.format_exc())
                
                #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
                self.parentWidget().parentWidget().parentWidget().busy('end')
                return -1
            else:
                sortedArray.sort()
                try:
                    len(sortedArray)
                except TypeError as e:
                    sortedArray = [sortedArray]
                
                filteredList = None
                for value in sortedArray:
                    value = str(value)
                    try:
                        if filteredList[len(filteredList)-1] != value:
                            filteredList.append(value)
                    except TypeError as e:
                        filteredList = [value]
                
                #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
                self.parentWidget().parentWidget().parentWidget().busy('end')
                
                return filteredList
        else:
            QtGui.QMessageBox.critical(self, 'bestfilter error', 'too many files\n' + str(bestfilter))
            return None
    
    def getPreviousFilter(self, filterDict):
        
        previousFiles = os.listdir(self.filterDir)
        for i in range(len(previousFiles)):
            previousFiles[i] = os.path.join(self.filterDir, previousFiles[i])
        
        tmpPrevFiles = list(previousFiles)
        
        for prevFile in tmpPrevFiles:
            
            if(not os.path.isfile(prevFile) or
              os.path.splitext(prevFile)[1] != '.csv' or
              os.path.getsize(self.fileName) != self.dataFileSize or
              os.path.getmtime(prevFile) < os.path.getmtime(self.fileName)): #mtime -> last modification time
                
                previousFiles.remove(prevFile)
        
        self.dataFileSize = os.path.getsize(self.fileName)
        
        def namesFromFilter(filterDict):
            names = [self.filterDir + os.sep + os.path.splitext(os.path.basename(self.fileName))[0] + '-']
            
            sortedkeys = filterDict.keys()
            sortedkeys.sort()
            print 'filterDict\n' + str(filterDict)
            for key in sortedkeys:
                newnames = []
                
                for name in names:
                    for filter in filterDict[key]:
                        newnames.append(name + '+' + key + '_' + str(filter))
                if len(newnames) != 0:
                    names = newnames
                    print 'namesfromfilter\n' + str(names) + '\n'
            
            for i in range(len(names)):
                names[i] += '.csv'
            
            return names
        
        names = namesFromFilter(filterDict)
        
        def comparefilter(newfilename, oldfilename):
                newfilename = os.path.splitext(os.path.basename(os.path.normpath(newfilename)))[0]
                oldfilename = os.path.splitext(os.path.basename(os.path.normpath(oldfilename)))[0]
                
                if newfilename == oldfilename:
                    return 0
                else:
                    newfilename = newfilename.split('-', 1)
                    oldfilename = oldfilename.split('-', 1)
                    
                    if newfilename[0] != oldfilename[0] or newfilename[1] == '':
                        return -1
                    else:
                        newfilename = newfilename[-1].split('+')
                        oldfilename = oldfilename[-1].split('+')
                        
                        if len(oldfilename) == 1:
                            return len(newfilename)
                        else:
                            filterMatch = len(newfilename)
                            for filter in oldfilename:
                                try:
                                    newfilename.index(filter)
                                    filterMatch -= 1
                                except ValueError as e:
                                    return -1
                            
                            return filterMatch
        bestfilter = []
        previousFiles.append(self.fileName)
        for i, currentFilterName in enumerate(names):
            bestfilter.append([currentFilterName, -1, self.fileName])
            for prevFile in previousFiles:
                num = comparefilter(currentFilterName, prevFile)
                if num > -1 and (num < bestfilter[i][1] or bestfilter[i][1] == -1):
                    bestfilter[i] = (currentFilterName, num, prevFile)
        
        return bestfilter
    
    def makeFilteredFile(self, filterDict, bestfilter):
        print 'bestfilter\n' + str(bestfilter)
        if bestfilter[1] == 0:
            return bestfilter[0]
        elif bestfilter[1] == -1:
            return bestfilter[2]
        else:
            def filter_check(filename, datalist):
                filename = os.path.splitext(filename)[0].split('-', 1)[-1].split('+')
                filename.remove('')
                for filter in filename:
                    sepfilter = filter.split('_')
                    
                    if float(sepfilter[1]) != float(datalist[self.headers.get(sepfilter[0])]):
                        return False
                
                return True
            
            try:
                oldfilter = open(bestfilter[2], 'r')
                newfile = open(bestfilter[0], 'w')
            except IOError as e:
                QtGui.QMessageBox.critical(self, 'File Error', 'Error occured while creating the filtered files.\n' +
                                                                repr(e) + '\n' + traceback.format_exc())
            else:
                print 'making ' + bestfilter[0]
                newfile.write(oldfilter.readline()) # writing headers
                for line in oldfilter:
                    linelist = line.strip().split(',')
                    if filter_check(bestfilter[0], linelist):
                        newfile.write(line)
            finally:
                oldfilter.close()
                newfile.close()
        
        return bestfilter[0]
    
    def getGraphableFiles(self):
        if self.filteringGroupBox.isChecked():
            bestfilter = self.getPreviousFilter(self.getFilteringChoice())
            filelist = []
            for onefilter in bestfilter:
                filelist.append([self.makeFilteredFile(self.getFilteringChoice(), onefilter), str(self.filterList[-1][0].currentText())])
        else:
            filelist = [[self.fileName, None]]
        
        return filelist
    
    def createFilteredFile(self):
        filterDict = self.getFilteringChoice()
        try:
            saveFile = QtGui.QFileDialog.getSaveFileName(self,'Save File', self.saveFilterLastDir, 'Comma Separated Values (*.csv)')
        except AttributeError:
            saveFile = QtGui.QFileDialog.getSaveFileName(self,'Save File', '', 'Comma Separated Values (*.csv)')
        
        saveFile = str(saveFile)
        if saveFile != '':
            #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
            self.parentWidget().parentWidget().parentWidget().busy('start')
            self.saveFilterLastDir = os.path.split(saveFile)[0]
            
            try:
                dataFile = open(self.fileName, 'r')
                filterFile = open(saveFile, 'w')
            except IOError as e:
                QtGui.QMessageBox.critical(self, 'File Error', repr(e))
            else:
                filterFile.write(dataFile.readline()) # headers
                for line in dataFile:
                    lineList = line.strip().split(',')
                    for key in filterDict.keys():
                        if float(lineList[self.headers.get(key)]) not in filterDict[key]:
                            break
                    else:
                        filterFile.write(line)
            finally:
                dataFile.close()
                filterFile.close()
                
                #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
                self.parentWidget().parentWidget().parentWidget().busy('end')
    
    def getFilteringChoice(self):
        filterDict = {}
        for widgetList in self.filterList:
            headerFilter = str(widgetList[0].currentText())
            if headerFilter != '--Filter--':
                if not filterDict.has_key(headerFilter):
                    filterDict[headerFilter] = []
                for value in widgetList[1].selectedItems():
                    filterDict[headerFilter].append(float(value.text()))
        
        return filterDict
    
    # # # # # # # # #
    # Dynamic Group #
    # # # # # # # # #
    def createDynamicGroup(self):
        self.dynamicGraphGroupBox = QtGui.QGroupBox("Dynamic Graph", self)
        self.dynamicGraphGroupBox.setCheckable(True)
        self.dynamicGraphGroupBox.setChecked(False)
        self.dynamicGraphGroupBox.setToolTip("Graphs a data file that is still being updated.")
        gridLayout = QtGui.QGridLayout(self.dynamicGraphGroupBox)
        
        
        self.newSegmentsCheckBox = QtGui.QCheckBox("Graph New Segments", self)
        
        self.separateDaysCheckBox = QtGui.QCheckBox("Separate Days", self)
        
        self.headerDayNumComboBox = QtGui.QComboBox(self)
        tempList = self.headers.keys()
        tempList.sort()
        tempList.insert(0, "--Day Column--")
        self.headerDayNumComboBox.addItems(tempList)
        
        
        #connect SIGNALs
        self.connect(self.dynamicGraphGroupBox, QtCore.SIGNAL('toggled(bool)'), self.dynamicToggled)
        
        #self.connect(self.separateDaysCheckBox, QtCore.SIGNAL('toggled(bool)'), self.dynamicToggled)
        #self.connect(self.separateDaysCheckBox, QtCore.SIGNAL('toggled(bool)'), self.plotButtonEnable)
        
        #self.connect(self.headerDayNumComboBox, QtCore.SIGNAL('activated(QString)'), self.plotButtonEnable)
        
        
        #Layout design
        gridLayout.addWidget(self.separateDaysCheckBox, 0, 0)
        gridLayout.addWidget(self.headerDayNumComboBox, 0, 1)
        
        gridLayout.addWidget(self.newSegmentsCheckBox, 1, 0)
        
        
        gridLayout.setRowStretch(2, 1)
        gridLayout.setColumnStretch(2, 1)
        
        
        self.dynamicGraphGroupBox.setLayout(gridLayout)
        
        return self.dynamicGraphGroupBox
    
    def dynamicToggled(self, checked=False):
        self.separateDaysCheckBox.setEnabled(checked)
        if checked:
            self.headerDayNumComboBox.setEnabled(self.separateDaysCheckBox.isChecked())
        else:
            self.separateDaysCheckBox.setChecked(False)
            
            self.stopDynamicClicked()
    
    # # # # # # # # # # # #
    # Graph Control Group #
    # # # # # # # # # # # #
    def createGraphControlGroup(self):
        groupBox = QtGui.QGroupBox("Graph Controls", self)
        hBoxLayout = QtGui.QHBoxLayout(groupBox)
        
        
        self.plotPushButton = QtGui.QPushButton("Plot", self)
        
        self.clearPushButton = QtGui.QPushButton("Clear Graph", self)
        
        self.stopDynamicPushButton = QtGui.QPushButton('Stop Dynamic', self)
        
        self.figureSpinBox = QtGui.QSpinBox(self)
        self.figureSpinBox.setRange(1, 10)
        self.figureSpinBox.setPrefix("Figure ")
        
        #connect SIGNALs
        self.connect(self.plotPushButton, QtCore.SIGNAL('clicked()'), self.plotClicked)
        
        self.connect(self.clearPushButton, QtCore.SIGNAL('clicked()'), self.clearClicked)
        
        self.connect(self.stopDynamicPushButton, QtCore.SIGNAL('clicked()'), self.stopDynamicClicked)
        
        
        #Layout design
        firstButtonsVBoxLayout = QtGui.QVBoxLayout()
        firstButtonsVBoxLayout.addWidget(self.plotPushButton)
        firstButtonsVBoxLayout.addWidget(self.clearPushButton)
        hBoxLayout.addLayout(firstButtonsVBoxLayout)
        
        figureStopVBoxLayout = QtGui.QVBoxLayout()
        figureStopVBoxLayout.addWidget(self.stopDynamicPushButton)
        figureStopVBoxLayout.addWidget(self.figureSpinBox)
        hBoxLayout.addLayout(figureStopVBoxLayout)
        
        
        groupBox.setLayout(hBoxLayout)
        
        return groupBox
    
    def plotButtonEnable(self):
        if (self.xaxisComboBox.currentText() != '--X-Axis--' and \
           (not self.separateDaysCheckBox.isChecked() or \
                self.headerDayNumComboBox.currentText() != '--Day Column--')):
            
            self.plotPushButton.setEnabled(True)
        
        else:
            self.plotPushButton.setEnabled(False)
    
    def get_settingsDict(self):
        settingsDict = {'filelist&filter': self.getGraphableFiles(),
                        'headerdict': self.getSelectedHeaders(),
                        'xaxis': str(self.xaxisComboBox.currentText()),
                        'dynamic': self.dynamicGraphGroupBox.isChecked(),
                        'multiple_axes': not self.singleGraphCheckBox.isChecked(),
                        'figure': self.figureSpinBox.value(),
                        'fig_title': self.get_fig_title(),
                        'fig_rowsize': self.columnSpinBox.value(),
                        'legend': self.showLegendCheckBox.isChecked(),}
        return settingsDict
    
    def plotClicked(self):
        settingsDict = self.get_settingsDict()
        
        lineDict = self.get_linestyle() 
        
        #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
        self.parentWidget().parentWidget().parentWidget().startPlotting(settingsDict, lineDict)
    
    def clearClicked(self):
        #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
        self.parentWidget().parentWidget().parentWidget().clearGraph(self.figureSpinBox.value())
        self.stopDynamicClicked()
    
    def stopDynamicClicked(self):
        #parent is tabWidget, tabwidget parent is stackedWidget, stackedWidget parent is MyWindow
        self.parentWidget().parentWidget().parentWidget().dynamicTimer.stop()
        self.parentWidget().parentWidget().parentWidget().busy('stop')
        
        print 'dynamic stopped'
    

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.grapher = graphFiles.mplQtGrapher()
        self.first_axes = None
        self.dynamicTimer = QtCore.QTimer(self)
        self.notbusy = True
        self.connect(self.dynamicTimer, QtCore.SIGNAL('timeout()'), self.dynamicPlot)
        self.loadFileLastDir = ''
        
        self.setWindowTitle("MAppleT Graphing Window")
        
        self.createCenterGraph()
        self.createActions()
        self.createMenus()
        #self.createToolBars()
        self.createStatusBar()
        
        self.loadFile()
    
    def createCenterGraph(self):
        self.centerWidget = QtGui.QTabWidget(self)
        self.centerWidget.setMovable(True)
        self.setCentralWidget(self.centerWidget)
    
    def createTab(self, fileName):
        self.centerWidget.setCurrentIndex(self.centerWidget.addTab(MySettingsTab(self.centerWidget, fileName),
                                                                   os.path.basename(fileName)))
    
    #Creates the actions for the menubar; e.g. File, Edit, Help etc.
    #Connects the action SIGNALs to the class functions
    def createActions(self):
        self.openAction = QtGui.QAction('&Open...', self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Load options for a data file.")
        self.connect(self.openAction, QtCore.SIGNAL('triggered()'), self.loadFile)
        
        self.closeTabAction = QtGui.QAction('Close Tab', self)
        self.closeTabAction.setShortcut("Ctrl+W")
        self.closeTabAction.setStatusTip("Closes the current tab.")
        self.connect(self.closeTabAction, QtCore.SIGNAL('triggered()'), self.closeTab)
        
        self.quitAction = QtGui.QAction('&Quit', self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip("Quit the application")
        self.connect(self.quitAction, QtCore.SIGNAL("triggered()"), self.close)
        
        self.helpAction = QtGui.QAction('&Help', self)
        self.connect(self.helpAction, QtCore.SIGNAL('triggered()'), self.help)
    
    #Creates the menubar and adds the menus and actions
    def createMenus(self):
        fileMenu = self.menuBar().addMenu('&File')
        
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.closeTabAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.quitAction)
        
        #self.menuBar().addAction(self.helpAction)
    
    # def createToolBars(self):
        # pass
    
    def createStatusBar(self):
        self.statusBar().showMessage(self.tr("Ready"))
    
    def loadFile(self):
        fileName = QtGui.QFileDialog.getOpenFileNames(self,'Data Files', self.loadFileLastDir, 'Comma Separated Values (*.csv)')
        fileName.sort()
        
        if fileName.count() > 0:
            self.loadFileLastDir = os.path.split(str(fileName.first()))[0]
        
        for path in fileName:
            self.createTab(os.path.normpath(str(path)))
    
    def closeTab(self):
        self.centerWidget.removeTab(self.centerWidget.currentIndex())
    
    #May provide general help later
    def help(self):
        QtGui.QMessageBox.information(self, 'Help', 'Currently there is no help. You are doomed.')
        #QtGui.QWhatsThis.enterWhatsThisMode()
    
    def startPlotting(self, settingsDict, lineDict):
        self.busy('start')
        try:
            for filePath, filtername in settingsDict['filelist&filter']:
                self.first_axes, axes_added = self.grapher.graph(filePath = filePath,
                                                                 xaxis = settingsDict['xaxis'],
                                                                 named_cols = settingsDict['headerdict'],
                                                                 legend = settingsDict['legend'],
                                                                 filtername = (filtername if filtername != '--Filter--' else None),
                                                                 first_axes = self.first_axes,
                                                                 multi_axes = settingsDict['multiple_axes'],
                                                                 figure = settingsDict['figure'],
                                                                 fig_title = settingsDict['fig_title'],
                                                                 clear_figure = settingsDict['dynamic'],
                                                                 fig_rowsize = settingsDict['fig_rowsize'])
            
                self.grapher.change_line_styles(figure = settingsDict['figure'],
                                                linewidth = lineDict['linewidth'],
                                                linestyle = lineDict['linestyle'],
                                                marker = lineDict['marker'],
                                                markersize = lineDict['markersize'],
                                                legend = settingsDict['legend'])
            
            if settingsDict['dynamic'] is True:
                self.dynamicTimer.start(1000)
        except IOError as ioe:
            QtGui.QMessageBox.critical(self, 'File Error', 'An error occured when using the file. ' +
                                                           'Check to make sure that the file exists and has the required data. ' + 
                                                           'This problem may be caused by an empty file.\n\n' +
                                                           repr(ioe) + '\n' + traceback.format_exc())
        except Exception as e:
            QtGui.QMessageBox.critical(self, 'Graphing Error', 'An error occured while trying to graph.\n\n' +
                                                                repr(e) + '\n' + traceback.format_exc())
        finally:
            self.busy('end')
    
    def dynamicPlot(self):
        self.busy('start')
        
        settingsDict = self.centerWidget.currentWidget().get_settingsDict()
        lineDict = self.centerWidget.currentWidget().get_linestyle()
        
        try:
            for filePath, filtername in settingsDict['filelist&filter']:
                self.first_axes, axes_added = self.grapher.graph(filePath = filePath,
                                                                 xaxis = settingsDict['xaxis'],
                                                                 named_cols = settingsDict['headerdict'],
                                                                 legend = settingsDict['legend'],
                                                                 filtername = (filtername if filtername != '--Filter--' else None),
                                                                 first_axes = self.first_axes,
                                                                 multi_axes = settingsDict['multiple_axes'],
                                                                 figure = settingsDict['figure'],
                                                                 useoldlines = settingsDict['dynamic'],
                                                                 fig_rowsize = settingsDict['fig_rowsize'])
            
                self.grapher.change_line_styles(figure = settingsDict['figure'],
                                                linewidth = lineDict['linewidth'],
                                                linestyle = lineDict['linestyle'],
                                                marker = lineDict['marker'],
                                                markersize = lineDict['markersize'],
                                                legend = settingsDict['legend'])
        except IOError as ioe:
            QtGui.QMessageBox.critical(self, 'File Error', 'An error occured when using the file. ' +
                                                           'Check to make sure that the file exists and has the required data. ' + 
                                                           'This problem may be caused by an empty file.\n\n' +
                                                           repr(ioe) + '\n' + traceback.format_exc())
            self.dynamicTimer.stop()
        except Exception as e:
            QtGui.QMessageBox.critical(self, 'Graphing Error', 'An error occured while trying to graph.\n\n' +
                                                                repr(e) + '\n' + traceback.format_exc())
            self.dynamicTimer.stop()
        gc.collect(0)
        
    def busy(self, text):
        if text == 'start' and self.notbusy:
            self.busyProgressBar = QtGui.QProgressBar(self)
            self.busyProgressBar.setRange(0, 0)
            self.busyProgressBar.setValue(0)
            
            self.statusBar().addWidget(self.busyProgressBar)
            
            self.notbusy = False
            self.repaint()
        
        elif text == 'end':
            self.statusBar().removeWidget(self.busyProgressBar)
            self.notbusy = True
    
    def clearGraph(self, figNum):
        self.grapher.clear_figure(figNum)
        self.first_axes = None


#creates and shows the qt window

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
