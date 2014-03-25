#-*- encoding: Latin-1 -*-

from mtg_to_qualitree import qualitree_nom_rameaux
from extraction_rameaux import *
def ram_mixtes_leaves(mtg_file_path):
    '''Renvoie un dictionaire avec en clés feuilles (identifiants d'amlPy) et en valeur le nom qualitree du rameau mixte auquel appartient cette feuille.'''
    
    m = MTG(mtg_file_path)
    plants = VtxList(Scale=1)
    
    annees = sorted(list(set([an(x) for x in uc(plants[0])])))

    ram_mixtes = ToSet(rameaux(plants[0]))#rameaux mixtes

    #Les rameaux mixtes doivent être des UC de l'année précédente, sinon la condition de qualitree comme quoi un rameau mixte ne peut pas porter de ramifications n'est pas respectée, hors des bugs de MAppleT peuvent entrainer que certaines feuilles ne tombent pas ou que plusieurs UC soient produites dans la même année, les rameaux non conformes sont supprimés. 
    ram_mixtes_error = [x for x in ram_mixtes if an(x) != annees[-2]]
    for r in ram_mixtes_error:
        print 'ERREUR : rameaux mixte ' + Class(r) + str(Index(r)) +  ' avec pour année de croissance ' + str(an(r)) + '. Ce rameau ne sera pas considéré comme mixte'
        
    ram_mixtes = [x for x in ram_mixtes if an(x) == annees[-2]]

    rm = ram_mixtes
    while True:
        rm_new = ToSet([Father(x) for x in rm] + rm)#On ajoutte le vieux bois
        if len(rm_new) == len(rm):#On s'arrête quand on ne trouve plus de nouveaux rameaux.
            break
        else:
            rm = rm_new
    rm = [x for x in rm if  x != None]

    noms_rameaux = qualitree_nom_rameaux(rm)
   
    dico = {}
    for R in ram_mixtes:
        F = []
        for pf in Sons(R):
            F += leaves(pf)
            for pb in Sons(pf):#Pousses de bourses
                F += leaves(pb)
        dico[noms_rameaux[R]] = [Feature(x, "lstring_id") for x in F  if la(x) > 0.]
   
    return dico

d=ram_mixtes_leaves(r'fuji_0_0_1998.mtg')
import pickle
F = open(r'dico_ram_mixtes_feuilles.pickle','wb')
pickler = pickle.Pickler(F)
pickler.dump(d)

raw_input()