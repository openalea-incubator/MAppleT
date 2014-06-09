import matplotlib as mpl
mpl.use('Qt4Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np

import os.path
import itertools


class mplQtGrapher():
    def __init__(self):
        '''creates color_cycle and marker_cycle from itertools.cycles
        for use when choosing colors and markers for lines.
        '''
        
        self.fig_titleTextDict = {}
        
        self.create_cycles()
        
        self.lineDescDict = {}
        for pair in plt.Line2D.lineStyles.items():
            self.lineDescDict[pair[1]] = pair[0]
    
    def create_cycles(self):
        '''
        creates color cycle and marker cycle
        '''
        tmp = [(i/4.0, j/4.0, k/4.0) for i in xrange(4)
                                     for j in xrange(4)
                                     for k in xrange(4)]
        
        #scrambling the color list so that similar
        #colors will not appear close together
        for i in xrange(2):
            tmp2 = []
            for j in xrange(5):
                tmp2 += tmp[j::5]
            tmp = tmp2
        self.color_cycle = itertools.cycle(tmp)
        
        self.marker_cycle = itertools.cycle(plt.Line2D.filled_markers)
    
    def graph(self, filePath, xaxis, named_cols, usecols=None, delimiter=',',
                    legend=True, filtername=None, figure=None, fig_title='',
                    clear_figure=False, useoldlines=False, first_axes=None,
                    multi_axes=True, fig_rowsize=None):
        '''filePath is a string that can be used to open a file with
            numpy.genfromtxt()
        xaxis is the column header of data column from the file being used for
            graphing
        named_cols is a dictionary of header names and their corresponding
            column number
        usecols are the numbers of the columns that will be used. if None, will
            use the numbers in named_cols
        delimiter is for indicating how the file is delimited, default is ','
        legend: if True, will display a legend on the matplotlib graphs. the
            line names come from the file basename and the header name
        filtername: used to create a line name from the filtered file name, if
            None, normal line naming is used.
        figure allows creating and switching to different mpl figures. if None,
            will create a new figure, otherwise must be a number of the figure
            you want.
        fig_title allows for a string to be placed at the top of the figure.
        clear_figure removes all previous information before graphing new info.
        useoldlines, if True, will attempt to match lines by their label and
            replace the data instead of creating an additional line.
        first_axes allows graphing on already existing axes. if None, will
            always use new axes for graphing.
        multi_axes allows for creating different axes for each header column.
            If False, will draw all lines on the same axes.
        fig_rowsize causes the axes on the figure to be oriented in a grid with
            a number of rows equal to fig_rowsize. if None, will use equal rows
            and columns to display the axes.
        '''
        # Getting the correct figure to plot on
        if figure is not None:
            plt.figure(figure)
        else:
            plt.figure()
            #figure = plt.get_fignums()[-1]
        
        if clear_figure:
            plt.clf()
        # Getting the correct axes to plot on
        prev_axes = len(plt.gcf().get_axes())
        
        if first_axes is None:
            first_axes = prev_axes + 1
        if (multi_axes and first_axes + len(named_cols)-2 > prev_axes or
            not multi_axes and first_axes > prev_axes):
            if multi_axes:
                rows = len(named_cols)-1 + prev_axes
                if fig_rowsize is None:
                    rows = np.sqrt(rows)
                    fig_rowsize = np.floor(rows)
                else:
                    rows /= float(fig_rowsize)
                rows = np.ceil(rows)
            else:
                if prev_axes > 0:
                    rows = prev_axes
                    if fig_rowsize is None:
                        rows = np.sqrt(rows)
                        fig_rowsize = np.floor(rows)
                    else:
                        rows /= float(fig_rowsize)
                    rows = np.ceil(rows)
                else:
                    rows = 1
                    fig_rowsize = 1
            rows = int(rows)
            
            for axes in plt.gcf().get_axes():
                oldrow, oldcol, num = axes.get_geometry()
                axes.change_geometry(rows, fig_rowsize, num)
        else:
            #print 'enough axes to use'
            rows, fig_rowsize, junk = plt.gca().get_geometry()
        
        plt.gcf().add_subplot(rows, fig_rowsize, first_axes)
        # Current figure and current axes now correct
        
        if named_cols is not None and usecols is None:
            usecols = []
            names = []
            skip_header = 1
            
            for key in named_cols:
                names.append(key)
                usecols.append(named_cols[key])
            
            data = np.genfromtxt(fname=filePath, delimiter=delimiter,
                                 skip_header=skip_header, usecols=usecols,
                                 names=names)
            
            names = list(data.dtype.names)
            #print 'names:\n' + str(names)
            #print 'xaxis\t' + str(xaxis)
            cleanxaxis = xaxis.replace('(','').replace(')','').replace(' ','_')
            
            names.remove(cleanxaxis)
            
            plt.gcf().canvas.set_window_title('figure %d - %s' % (figure, os.path.basename(os.path.splitext(filePath)[0]).split('-', 1)[0]))
            
            #print rows, fig_rowsize
            i = 0
            for i, header in enumerate(names):
                label = None
                
                if filtername is None:
                    label = os.path.basename(os.path.splitext(filePath)[0]).split('+')[-1]
                else:
                    for name in os.path.basename(os.path.splitext(filePath)[0]).split('+'):
                        if filtername in name:
                            label = name.replace('_', ' ')
                            break
                    else:
                        label = os.path.basename(os.path.splitext(filePath)[0]).split('+')[-1]
                
                if multi_axes:
                    plt.gcf().add_subplot(rows, fig_rowsize, first_axes + i)
                    plt.ylabel(header)
                else:
                    label += header.replace('_', ' ')
                
                if useoldlines:
                    for line in plt.gca().get_lines():
                        if line.get_label() == label:
                            line.set_data(data[cleanxaxis], data[header])
                            plt.gca().relim()
                            plt.gca().autoscale()
                            break
                    else:
                        useoldlines = False
                
                if not useoldlines:
                    plt.plot(data[cleanxaxis], data[header],
                             color=self.color_cycle.next(), label=label)
                if legend:
                    plt.legend(prop=font_manager.FontProperties(size=8),
                               loc='best', ncol=2, borderaxespad=0)
                plt.xlabel(xaxis)
                plt.grid(True)
        
        if figure is not None:
            try:
                self.fig_titleTextDict[figure].set_text(fig_title)
            except KeyError as e:
                self.fig_titleTextDict[figure] = plt.gcf().suptitle(fig_title)
                self.fig_titleTextDict[figure].set_size(20)
        
        plt.show()
        plt.draw()
        
        return first_axes, i
    
    # def get_fignums(self):
        # return plt.get_fignums()
    
    # def get_figure_axes(self, figure):
        # axes=None
        # for figure in plt.get_fignums():
            # axes = len(plt.figure(figure).get_axes())
        
        # return axes
    
    def rename_figure(self, title, figure=None):
        '''title is a string that will be displayed at the top of the figure
        figure is the number of the figure whose title will be changed
            if None, will use current figure.
        '''
        if figure is not None:
            plt.figure(figure)
        plt.gcf().suptitle(title)
        plt.show()
        plt.draw()
    
    def change_line_styles(self, figure=None, linewidth=None, linestyle=None,
                           marker=False, markersize=None, legend=True):
        '''figure is the figure whose lines will be styled. if None, will use
            current figure.
        linewidth changes the width of the lines to be linewidth pixels.
            if None, no change. If 0 (zero), then no line will be displayed.
            However, markers will be displayed at every datapoint.
        linestyle changes the line type: such as dotted, dashed or solid. if
            None, no change.
        marker: if True, places markers on a datapoints in the line. marker
            type is random. if None, no change.
        markersize changes the size of the markers. if None, no change.
        legend: if True, will display a legend on the matplotlib graphs. The 
            line names come from the file basename and the header name.
        '''
        if figure is not None:
            plt.figure(figure)
        
        for axes in plt.gcf().get_axes():
            for line in axes.get_lines():
                if linewidth is not None:
                    line.set_linewidth(linewidth)
                if linestyle is not None:
                    line.set_linestyle(self.lineDescDict[linestyle])
                if marker:
                    #if line.get_marker() == 'None': #DDS commented, was keeping marker to be displayed ??
                    line.set_marker(self.marker_cycle.next())
                    line.set_markeredgewidth(0)
                    if line.get_linewidth() > 0:
                        line.set_markevery(len(line.get_xdata())//16)
                    else:
                        line.set_markevery(None)
                    if markersize is not None:
                        line.set_markersize(markersize)
                else:
                    line.set_marker('None')
            if legend:
                axes.legend(prop=font_manager.FontProperties(size=8),
                            loc='best', ncol=2, borderaxespad=0)
        
        plt.show()
        plt.draw()
    
    def clear_figure(self, figure=None):
        '''figure is the number that identifies the figure that will be cleared.
            if None, will clear current figure.
        '''
        if figure is not None:
            plt.figure(figure)
        plt.clf()
        self.create_cycles() #reset cycles
        self.fig_titleTextDict = {}
        plt.show()
        plt.draw()
