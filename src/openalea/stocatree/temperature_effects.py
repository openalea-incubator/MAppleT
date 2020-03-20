#-------------------------------------------------------------------------------
# Name:        temperature_effects
# Purpose:
#
# Author:       Han
#
# Created:     10/05/2011
# Copyright:   (c) Han 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import xlrd
#xlrd is a module to extract data from M$ excel files, should be replaced by csv
import datetime
from math import exp
import calendar

class Tp_date(object):
    def __init__(self, onset_year = 1994,
                    optimal_temperature = 1.1,
                    chilling_effect_interval = 20,
                    chilling_effect_onset_month = 10,
                    chilling_effect_onset_day = 30,
                    chilling_quantity_required = 56,
                    characteristic_temperature = 9.0,
                    heat_sigmoidal = False,
                    sigmoidal_slope = 6.0,
                    heat_quantity_required = 83.58):

        self.onset_year = onset_year
        self.optimal_temperature = optimal_temperature
        self.chilling_effect_interval = chilling_effect_interval
        self.chilling_effect_onset_month = chilling_effect_onset_month
        self.chilling_effect_onset_day = chilling_effect_onset_day
        self.chilling_quantity_required = chilling_quantity_required
        self.characteristic_temperature = characteristic_temperature
        self.heat_sigmoidal = heat_sigmoidal
        self.sigmoidal_slope = sigmoidal_slope
        self.heat_quantity_required = heat_quantity_required

        self.temp_file = xlrd.open_workbook("../../share/data/temperature_data.xls")
        self.temp_sheet = self.temp_file.sheet_by_name("moy")

        self.chilling_accummulation = 0
        self.heat_accummulation = 0

        self.dormancy_break_date = None
        self.bud_break_date = None

    def bud_break(self):
        for i in range(1, self.temp_sheet.nrows):
            dt_tuple = xlrd.xldate_as_tuple(self.temp_sheet.cell(i,0).value, 0)
            dt = datetime.datetime(*dt_tuple)
            if dt.month == self.chilling_effect_onset_month and dt.day == self.chilling_effect_onset_day:
                r_onset = i
                break
        for j in range(1, self.temp_sheet.ncols):
            if self.temp_sheet.cell(0,j).value == self.onset_year:
                c_onset = j
                break
        for k in range(r_onset, self.temp_sheet.nrows):
            tp_k = self.temp_sheet.cell(k, c_onset).value
            if tp_k > self.optimal_temperature - self.chilling_effect_interval and tp_k < self.optimal_temperature + self.chilling_effect_interval:
                ce = 1 - abs(tp_k - self.optimal_temperature)/self.chilling_effect_interval
                """
                if tp_k > self.optimal_temperature:
                    ce = 1 - (tp_k - self.optimal_temperature)/self.chilling_effect_interval
                else:
                    ce = 1 - (self.optimal_temperature - tp_k)/self.chilling_effect_interval
                """
            else:
                ce = 0
            self.chilling_accummulation += ce
            #print self.chilling_accummulation, xlrd.xldate_as_tuple(self.temp_sheet.cell(k,0).value, 0)[1], xlrd.xldate_as_tuple(self.temp_sheet.cell(k,0).value, 0)[2]
            if self.chilling_accummulation >= self.chilling_quantity_required:
                r_dormancy_break = k
                #print "dormancy_date: ", xlrd.xldate_as_tuple(self.temp_sheet.cell(r_dormancy_break,0).value, 0)[1], xlrd.xldate_as_tuple(self.temp_sheet.cell(r_dormancy_break,0).value, 0)[2]
                dbd_tuple = xlrd.xldate_as_tuple(self.temp_sheet.cell(r_dormancy_break,0).value, 0)
                dbd = datetime.datetime(*dbd_tuple)
                if dbd.month < self.chilling_effect_onset_month:
                    if calendar.isleap(self.onset_year) and dbd.month > 2:
                        self.dormancy_break_date = (self.onset_year, dbd.month, dbd.day-1, 0, 0)
                    else:
                        self.dormancy_break_date = (self.onset_year, dbd.month, dbd.day, 0, 0)
                else:
                    self.dormancy_break_date = (self.onset_year-1, dbd.month, dbd.day, 0, 0)
                break

        for p in range(r_dormancy_break+1, self.temp_sheet.nrows):
            tp_p = self.temp_sheet.cell(p, c_onset).value
            if self.heat_sigmoidal == False:
                he = exp(tp_p/self.characteristic_temperature-1)
            else:
                he = 2 / (1 + exp((tp_p - self.characteristic_temperature) / self.sigmoidal_slope))
            self.heat_accummulation += he
            if self.heat_accummulation >= self.heat_quantity_required:
                r_bud_break = p
                break

        # Get the date for bud break
        br_tuple = xlrd.xldate_as_tuple(self.temp_sheet.cell(r_bud_break, 0).value, 0)
        br = datetime.datetime(*br_tuple)
        if br.month < self.chilling_effect_onset_month:
            if calendar.isleap(self.onset_year) and br.month > 2:
                self.bud_break_date = (self.onset_year, br.month, br.day-1, 0, 0)
            else:
                self.bud_break_date = (self.onset_year, br.month, br.day, 0, 0)
            return self.bud_break_date
        else:
            self.bud_break_date = (self.onset_year-1, br.month, br.day, 0, 0)
            return self.bud_break_date

class Test(object):
    def __init__(self, first_year=1963, last_year=2010):
        t = open("dates_test.csv", "w")
        t.write("year, dormancy_break, bud_break\n")
        t.close()

        t = open("dates_test.csv", "a")
        for y in range(first_year, last_year+1):
            tp_date = Tp_date(onset_year=y)
            dt = tp_date.bud_break()
            t.write(str(y) + ",")
            t.write(str(tp_date.dormancy_break_date[2]) + "/" + str(tp_date.dormancy_break_date[1]) + ",")
            t.write(str(tp_date.bud_break_date[2]) + "/" + str(tp_date.bud_break_date[1]) + "\n")
        t.close()










