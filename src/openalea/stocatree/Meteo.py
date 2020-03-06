#### test
#!/usr/bin/env python
import numpy   as np
import datetime
import time
from math import * 



class meteo(object):
    
    def __init__(self, file_name):
        
        global Altitude
        global lat
        Altitude = 0
        
        lat = 45
         ### To modify, needs to be included in the parameter file.
         
        self.complete_file = np.loadtxt(file_name)
        #self.complete_file = np.genfromtxt(file_name,dtype='str')
        #self.complete_file = np.fromfile(file_name)
        self.file_dico  = {}
        self.premier_jour = datetime.date(int(self.complete_file[0,2]),int(self.complete_file[0,1]),int(self.complete_file[0,0]))
        
        for i in range(0,(len(self.complete_file))):
            dict_jour = {}
            date = datetime.date(int(self.complete_file[i,2]),int(self.complete_file[i,1]),int(self.complete_file[i,0]))
            dict_jour['jour_julien'] = self.compute_jour_julien(int(self.complete_file[i,2]),int(self.complete_file[i,1]),int(self.complete_file[i,0]))
            dict_jour['Tmax'] = self.complete_file[i,3]
            dict_jour['Tmin'] = self.complete_file[i,4]
            dict_jour['Hrmax'] = self.complete_file[i,5]
            dict_jour['Hrmin'] = self.complete_file[i,6]
            dict_jour['windspeed'] = self.complete_file[i,7]
            dict_jour['Rg'] = self.complete_file[i,8]
            dict_jour['Rainfall'] = self.complete_file[i,9]
            self.file_dico[date] = dict_jour
        
    def get_meteo_jour(self,jour) :
        return(self.file_dico[jour])
        
        
    def make_meteorological_calculation(self) :
        
        for key in sorted(self.file_dico):
            dict_jour = self.file_dico[key]
            
            dict_jour['VPD'] = self.computeVPD(dict_jour['Tmax'],dict_jour['Tmin'],dict_jour['Hrmax'], dict_jour['Hrmin'], dict_jour['jour_julien'],dict_jour['Rg'])
            dict_jour['ET0'] = self.computeET0(dict_jour['Tmax'],dict_jour['Tmin'], dict_jour['jour_julien'],dict_jour['Rg'],dict_jour['VPD'],dict_jour['windspeed'] )
        write_meteo_data("meteo_data.txt", self.premier_jour, self.file_dico)
        
    def compute_jour_julien(self, year, month, day ) :
        t= time.mktime((year, month, day, 1, 0, 0, 0, 0, 0))
        return(time.gmtime(t)[7])

    def computeVPD(self, Tmax, Tmin, RHmax, RHmin, jour_julien, Rg) :
        
        global ea
        global esat
        
        TMoy = (Tmax + Tmin) / 2
        HMoy = (RHmin + RHmax ) / 2
        if Tmin > Tmax :
            Tmax = Tmin
        if RHmin > RHmax : 
            RHmax = RHmin
        
        esat = 0.3054 * (exp(17.24 * Tmax/ ( Tmax + 237.3)) + exp(17.27 * Tmin/(Tmin + 237.3)))
        ea = 0.3054 * (exp(17.27 * Tmax/(Tmax + 237.3))* RHmin / 100 + exp(17.27 * Tmin / (Tmin + 237.3))* RHmax/100)
        VPD = esat - ea
        return(VPD)
       
     
    def computeET0(self, Tmax, Tmin, jour_julien, Rg, VPD, windspeed) :    
        
        
        lat_rad = lat*pi/180
        
        Decli = 0.409*sin(0.0172 * jour_julien-1.39)
        SunPos = acos( - tan( lat_rad ) * tan(Decli))  
        Sundist = 1 + 0.033*cos( 2 * (pi/365) * jour_julien )
        Ray_extra = 24 * 60 * 0.0820 / pi * Sundist * (SunPos * sin(Decli) * sin(lat_rad) + cos(Decli)* cos(lat_rad) * sin(SunPos) )
        RGMax = ( 0.75 + 0.00002 * Altitude ) *   Ray_extra
        day_lenght = 7.64 * SunPos
        PAR = 0.48 * Rg
        if Rg > RGMax :
            ratioRg = 1
        else :
            ratioRg = Rg / RGMax
        
        Rn = 0.77*Rg - (1.35* ratioRg -0.35)*(0.34-0.14*(ea)**(0.5))*((Tmax +273.16)**4+(Tmin +273.16)**4)*2.45015*10**(-9)
        TMoy = (Tmin + Tmax)/2
        Tlat = 2.501-2.361*10**(-3)*TMoy 
        pent_vap_sat = 4098 * (0.6108*exp(17.27 * TMoy /(TMoy +237.3)))/((TMoy +237.3)**2)
        Kpsy = 0.00163 * 101.3 * (1-(0.0065*Altitude/293))**5.26
        erad = 0.408 * Rn*pent_vap_sat/(pent_vap_sat+Kpsy*(1+0.34*windspeed))
        eaero = ((900/(TMoy +273.16))*(( esat - ea)* windspeed)*Kpsy)/(pent_vap_sat+Kpsy*(1+0.34*windspeed))
        ET0 = erad + eaero
        return(ET0)
    
    
    

def write_meteo_data(chemin,first_day,dico) :
        f=open(chemin,"w")
        f.write("day" + '\t')
        for key_2 in dico[first_day] :    #### doing that we can easily add new computed variables in the ouput file
            f.write(str(key_2) + '\t')
        f.write("\n")
        
        
        for key in sorted(dico):
            f.write(str(key) + '\t')
            for key_2 in dico[key] :
                f.write(str(dico[key][key_2]) + '\t')
            f.write('\n')
        f.close()
def pri():
    print('toto')

        
def convert_datetime_date_datetime_datetime(date) :
    d = datetime.datetime(date.year,date.month,date.day)
    return(d)

class Storm(object):

  def __init__(self):
    lightnings = 2
    thunder = 2

  def startFire(self):
    pass

