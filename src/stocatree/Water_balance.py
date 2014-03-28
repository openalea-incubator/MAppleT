#!/usr/bin/env python

from Meteo import *
import datetime


class simplified_water_balance(object):
    
    def __init__(self, meteo_file, field_capacity = 0.23, ini_water_content = 0.22): ## (mm.mm-1) to be assigned in a parameter file
        self.meteo_file = meteo(meteo_file)
        self.meteo_file.make_meteorological_calculation()
        
        #self.crop_coefficient_choice = "single_crop_coefficient"  ### 'dual_crop_coefficient', 'single_crop_coefficient", "radiation_interception"  These parameters should be read in a parameter file
        #self.soil_representation_choice = "single_compartment"   ### 'two_compartment layers'
        self.kc = 0
        self.TTSW = compute_water_content_one_compartment(current_water_content = field_capacity)
        self.ASW = compute_water_content_one_compartment(current_water_content = ini_water_content)
        self.FTSW = compute_FTSW(self.ASW,self.TTSW)
        self.result_dico = {}
        self.ks = 0
        self.ETR = 0
        
    
        
    def independant_calculation(self):
        for key in sorted(self.meteo_file.file_dico) :
            self.calcule_BH_jour(key)
        
    def calcule_BH_jour(self, jour) :
        self.kc = compute_single_crop_coefficient(self.meteo_file.file_dico[jour]['jour_julien'])
        self.ks = compute_coeff_stress_simple(self.FTSW)
        self.ETR = compute_ETR_global(self.kc,self.meteo_file.file_dico[jour]['ET0'], self.ks) 
        resultat_avant_drainage = water_balance_equation(self.ASW,self.meteo_file.file_dico[jour]['Rainfall'], self.ETR) 
        if resultat_avant_drainage > self.TTSW :
            self.ASW = self.TTSW
        else :
            self.ASW = resultat_avant_drainage
        self.FTSW = compute_FTSW(self.ASW,self.TTSW)
        dict_jour = {}
        dict_jour['ETR'] = self.ETR
        dict_jour['ASW'] = self.ASW
        dict_jour['FTSW'] = self.FTSW
        dict_jour['ET0'] = self.meteo_file.file_dico[jour]['ET0']
        dict_jour['kc'] = self.kc
        dict_jour['ks'] = self.ks
        dict_jour['Rainfall'] = self.meteo_file.file_dico[jour]['Rainfall']
        self.result_dico[jour] = dict_jour
        #for key in self.meteo_file.file_dico:
        #    print(self.k)
        #    if self.meteo_file.file_dico[key]['jour_julien'] < 150 :
        #        self.k = 2
        #    elif self.meteo_file.file_dico[key]['jour_julien'] < 200 :
        #        self.k = 3
        #    else :
        #        self.k = 0
        #
    def whole_dataset_results(self):
        write_meteo_data("BH_results.txt",self.meteo_file.premier_jour,self.result_dico) ### function of meteo.py    
        



        
def compute_ETR_global(kc,ET0,coeff_stress):
    ETR = ET0 * coeff_stress * kc
    return(ETR)
    
def compute_coeff_stress_simple(FTSW, seuil_FTSW = 0.4):
    if FTSW < seuil_FTSW :
        ks = FTSW/seuil_FTSW
    else :
        ks = 1
    return(ks)

        
        
def compute_water_content_one_compartment(prof_rac = 1000, wilting_point=0.10, current_water_content = 0.23):
    water_content = ( current_water_content - wilting_point) *  prof_rac
    return(water_content)
    

def water_balance_equation(Available_soil_water, Rainfall,ETR, irrigation=0, streaming_in=0,streaming_out=0 ) :
    ASW = Available_soil_water + Rainfall + irrigation - ETR  + streaming_in - streaming_out
    return(ASW)

def compute_FTSW(ASW,TTSW) :
    FTSW = ASW/TTSW
    return(FTSW)


def compute_single_crop_coefficient(date_jour_julien,ini=0.2,mid=0.8,end=0.6,date_beginning_dev =90,date_end_vege= 150, date_senescence_beginning = 190, dateend=250) :
    if date_jour_julien < date_beginning_dev :
        k= ini
    elif date_jour_julien < date_end_vege :
        k  = (mid - ini) /(date_end_vege - date_beginning_dev ) * (date_jour_julien-date_beginning_dev)  + ini
    elif date_jour_julien < date_senescence_beginning :
        k = mid
    elif date_jour_julien < dateend :
        k = -(end - mid )/(date_senescence_beginning -  dateend) * (date_jour_julien-date_senescence_beginning) + mid
    else :
        k = ini
    return(k)
    
        
#def write_data(chemin,first_day,dico) :
#        f=open(chemin,"w")
#        f.write("day" + '\t')
#        for key_2 in dico[first_day] :    #### doing that we can easily add new computed variables in the ouput file
#            f.write(str(key_2) + '\t')
#        f.write("\n")
#        
#        
#        for key in sorted(dico):
#            f.write(str(key) + '\t')
#            for key_2 in dico[key] :
#                f.write(str(dico[key][key_2]) + '\t')
#            f.write('\n')
#        f.close()    

def compute_dual_crop_coefficient(ini,mid,end,datemin,datemax) :
    pass

def evolutive_cropcoefficient():
    pass

