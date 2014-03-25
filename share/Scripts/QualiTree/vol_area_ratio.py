#-*- encoding: Latin-1 -*-
'''Dans le calcul du taux de respiration (MRR), des données exprimées en fonction de l'aire des arbres sont disponibles
hors qualitree exprime MRR en fonction de la masse sêche d'où la nécessité de calculer un ratio surface/volume'''

from extraction_rameaux import *

def surf_vol(mtg_file_path):
    '''renvoie un tuple (surface, volume)'''
    m = MTG(mtg_file_path)
    plant = VtxList(Scale=1)[0]
    ucs = uc(plant)
    annees = sorted(list(set([an(x) for x in ucs])))
    UCS = {'all' : ucs, '0year' : [x for x in ucs if an(x) == annees[-1]], '1year' : [x for x in ucs if an(x) == annees[-2]], '2+years' : [x for x in ucs if an(x) in annees[0:-2]]}
    VS = {}
    for k,ucs in UCS.items():
        vol = sum([vol_uc(u) for u in ucs])
        surf = sum([area(u) for u in ucs])
        VS[k] = {'S':surf,'V':vol,'S/V' : surf/vol if vol > 0 else None}
    
    return VS

#sv = {mtg : surf_vol(mtg) for mtg in ['23_95.mtg','23_96.mtg','23_98.mtg','0_95.mtg','0_96.mtg','0_97.mtg','230_95.mtg','230_96.mtg']}
#F = open('SVratio.csv','w')
#F.write(';'+';'.join(sv.keys()) + '\n')
#for age in ['0year','1year','2+years']:
#    F.write(age + ';' + ';'.join([str(sv[mtg][age]['S/V']) for mtg in sv.keys()]) + '\n')

from glob import glob
dossier = r'C:\Users\Olivier\Desktop\mtg_fuji\*'
mtgs = [r"C:\Users\Olivier\Dropbox\APMed\Qualitree\lumiere\Fuji_0\1998_5_15\0.mtg",r"C:\Users\Olivier\Dropbox\APMed\Qualitree\lumiere\Fuji_1\1998_5_15\1.mtg",r"C:\Users\Olivier\Dropbox\APMed\Qualitree\lumiere\Fuji_2\1998_5_15\2.mtg",r"C:\Users\Olivier\Dropbox\APMed\Qualitree\lumiere\Fuji_2\1998_5_15\2.mtg"]
annees = [1998,1998,1998,1998]
mtgs,annees = zip(*[(mtg,annee) for mtg,annee in zip(mtgs,annees) if annee >= 96])#On enlève les arbres trop jeunes (pas de vieux bois)
arbres = ["F1","F2","F3","F4"]
sv0, sv1, sv2p = zip(*[(sv['0year']['S/V'],sv['1year']['S/V'],sv['2+years']['S/V']) for sv in [surf_vol(mtg) for mtg in mtgs]])
F = open('sv.csv','w')
F.write('arbre;annee;sv0;sv1;sv2p\n')
F.write('\n'.join([';'.join([arbre,str(annee),str(sv0e),str(sv1e),str(sv2pe)]) for arbre,annee,sv0e,sv1e,sv2pe in zip(arbres,annees,sv0,sv1,sv2p)]))
        
raw_input()
