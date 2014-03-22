#!/usr/bin/eval PYTHON_VERSION=2.6
#-*- encoding: Latin-1 -*-

#from extraction_rameaux import *
from openalea.mtg.aml import *
from math import pi

#===========================================================#
# Utils functions to explore and extract data from MTG      #
#===========================================================#


#**************
# Access to Feature
#**************
def an(x):
  """
    Returns the year of growht of elmt x
  """
  return Feature(x, "year")
 
def radius(x) :
  """
  Return the radius [m]
  """
  return Feature(x, "radius")

def topdia(x):
  """
  Return the top diameter [mm] (=radius*2000)
  """
  return Feature(x, "TopDia")

def rad(x) :#en mm!
  """
  Return the radius [mm]
  """
  return topdia(x)/2.0

def la(x) :
  """
    Returns the leaf_area value when exists, None/Undef otherwise
  """
  return Feature(x, "leaf_area")

def length(x):
  """
  Return the length [m]
  """
  return Feature(x, "length")
 
def xx(x):
  """
  Return the X position [m]
  """
  return Feature(x, "XX")

def yy(x):
  """
  Return the Y position [m]
  """
  return Feature(x, "YY")

def zz(x):
  """
  Return the Z position [m]
  """
  return Feature(x, "ZZ")


#*************

def uc(p) :
  """
    Returns all components of elmt p that are with Scale=2, i.e. growth unit
  """
  return Components(p, Scale=2)
  
def class_uc(x):
  """
    Transform class of x from G to 1, I to 2 and everything else to 0
  """
  if Class(x) == "G" :
      return 1
  else :
    if Class(x) == "I" :
      return 2
    else :
      return 0

def metamer(p):
  """
    Returns all scale 3 components of p, i.e. all metamers of p
  """
  return Components(p, Scale=3)

def uc1_leafy(p):
  """
  Returns GUs with growing leaves, actually with leaf on the first metamer growing,
  except for bourse shoot
  """
  return [x for x in uc(p) if la(Components(x)[0]) > 0.0 and Class(Father(x))!='I']

def rameaux(p):
  """
  Returns the Fruiting Units, i.e. shoots bearing leafy shoots and fruits
  """
  return list(set([Father(x) for x in uc1_leafy(p) if Father(x) != None]))

def type_uc(x):
  """
  Return the shoot category of UC, i.e. small, medium or large 
  """
  return Feature(metamer(x)[0], 'observation')

def nb_leafy_rameau_cat(x, cat):
  """
  Return the number of leafy shoots of category `cat` of a FU
  Note that bourse counts as 1 small leafy shoot
  """
  nb = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        nb +=1
      try:
        if type_uc(Sons(y)[0]) == cat:
          nb +=1
      except IndexError:
        continue
    elif type_uc(y) == cat:
      nb += 1
  return nb

def nb_leafy_rameau(x):
  """
  Return the total number of leafy shoots of a FU
  Note that bourse counts as 1 small leafy shoot
  """
  return sum([nb_leafy_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def fruit_nb(x):
  """
  Return the number of fruits on a GU
  """
  return len([y for y in metamer(x) if Feature(y, 'fruit')])

def fruit_ms(x):
  """
  Return the dry weight of fruits on a GU
  """
  return sum([Feature(y, 'fruit') for y in metamer(x) if Feature(y, 'fruit')])

def fruit_ram(x):
  """
  Return the total number of fruits on a FU
  """
  return sum([fruit_nb(y) for y in Sons(x)])

def fruit_ram_ms(x):
  """
  Return the total dry weight of fruits on a FU
  """
  return sum([fruit_ms(y) for y in Sons(x)])

def la_uc(x):
  """
  Returns the total leaf area of given GU
  """
  return sum([la(y) for y in metamer(x)])

def la_rameau_cat(x, cat):
  """
  Return the cumulated leaf area of all leafy shoots of category `cat` of a FU
  """
  la = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        la += la_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          la += la_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      la += la_uc(y)
  return la

def la_rameaux(x):
  """
  Return the cumulated length of all shoots of a FU
  """  
  return sum([la_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def length_uc(x):
  """
  Return the length of a GU
  """
  return sum(length(m) for m in metamer(x))

def length_rameau_cat(x, cat):
  """
  Return the cumulated length of all leafy shoots of category `cat` of a FU
  """
  length = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        length += length_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          length += length_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      length += length_uc(y)
  return length

def lencumul_ram(x):
  """
  Return the cumulated length of all shoots of a FU
  """  
  return sum([length_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

def vol(x):
  """
  Return the volume of the metamer x
  """
  return pi*(topdia(x)/2000.)**2 * length (x)


def vol_uc(x):
  """
  Return the volume of a GU
  """
  return sum([vol(m) for m in metamer(x)])

def vol_pousse(x):
  """
  Return the volume of a shoot, i.e. in case of bourse it returns the 
  cumulated volume of the shoot and all the bourse shoots
  """
  if Class(x) =="I" and Sons(x) != []:
    return vol_uc(x) + sum([vol_uc(y) for y in Sons(x)])
  else:
    return vol_uc(x)	

def vol_rameau_cat(x, cat):
  """
  Return the cumulated volume of all leafy shoots of category `cat` of a FU
  """
  vol = 0
  for y in Sons(x):
    if Class(y) == 'I':
      if cat == 'small':
        vol += vol_uc(y)
      try:
        if type_uc(Sons(y)[0]) == cat:
          vol += vol_uc(Sons(y)[0])
      except IndexError:
        continue
    elif type_uc(y) == cat:
      vol += vol_uc(y)
  return vol


def vol_rameaux(x):
  """
  Return the cumulated volume of all shoots of a FU
  """  
  return sum([vol_rameau_cat(x, cat) for cat in ['small', 'medium', 'large']])

#===========================================================#

def tree_sql(nom_arbre, date, variete, vr_masse_seche, jr_masse_seche, vb_masse_seche, architecture,rameauxmixte):
    """
        Génère le code sql permettant de supprimer un arbre dans la base de donnée de qualitree
        Renvoie la requête SQL en string
        nom_arbre (str) : nom de l'arbre dans la base de données qualitree
        date (str) : date à laquelle l'arbre à été mesuré sous la forme YYYY-MM-DD
        variete (str) : variété
        vr_masse_seche (float) : masse sèche des vielles racines (grammes)
        jr_masse_seche (float) : masse sèche des jeunes racines (grammes)
        vb_masse_seche (float) : masse sèche du vieux bois (grammes)
        architecture (list of list) : liste de listes représentant les rameaux mixtes et le vieux bois sous la forme : niveau (int), nom_rameau (str), diametre_base, diametre_ext, metamere, x1, y1, z1, x2, y2, Z2
        rameauxmixte (list of list) : liste de listes représentant les rameaux mixtes sous la forme : nom_rameau, tl_masse_seche, f2_nombre_unites, f2_masse_seche, pfx_nombre_unites, pfx_masse_seche
     """

    #Si il y a un arbre du même nom et année, on le supprime.
    sql = "DELETE FROM arbre WHERE nom_arbre='"+nom_arbre+"';\n"
    sql+= "DELETE FROM architecture WHERE nom_arbre='"+nom_arbre+"';\n"
    sql+= "DELETE FROM rameauxmixte WHERE nom_arbre='"+nom_arbre+"';\n"

    #table "arbre"
    header = ['nom_arbre', 'date', 'variete', 'vr_masse_seche', 'jr_masse_seche', 'vb_masse_seche']
    sql+= insert_into("arbre",header,[{'nom_arbre':nom_arbre, 'date':date, 'variete':variete, 'vr_masse_seche':vr_masse_seche, 'jr_masse_seche':jr_masse_seche, 'vb_masse_seche':vb_masse_seche}])

    #table "architecture" (géométrie rammeaux mixte + vieux bois)
    header = ['nom_arbre','niveau', 'nom_rameau', 'annee', 'diametre_base', 'diametre_ext', 'metamere', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'longueur']
    ins_architecture = [{'nom_arbre':nom_arbre,'niveau':rameau[0], 'nom_rameau':rameau[1], 'annee':int(date.split("-")[0]), 'diametre_base': rameau[2], 'diametre_ext' : rameau[3], 'metamere' : rameau[4], 'x1' :rameau[5], 'y1':rameau[6], 'z1':rameau[7], 'x2':rameau[8], 'y2':rameau[9], 'z2':rameau[10], 'longueur':rameau[11]} for rameau in architecture]
    sql+= insert_into("architecture",header,ins_architecture)
    
    #table "rameauxmixte" (matière sèche, concentration en sucres, nombre de pousses feuillées et de fruits...).
    header = ['nom_arbre', 'nom_rameau', 'date', 'tl_masse_seche', 'f2_tms_pulpe','f2_concent_sorbitol', 'f2_concent_sucrose', 'f2_concent_glucose', 'f2_concent_fructose', 'f2_nombre_unites', 'f2_masse_seche', 'pf1_nombre_unites', 'pf1_masse_seche', 'pf2_nombre_unites', 'pf2_masse_seche', 'pf3_nombre_unites', 'pf3_masse_seche']
    valeurs_sucres = (0.0018, 0.0104, 0.0185, 0.0182)#Valeurs "bidon" de teneur en sucre des fruits (nécessaire pour le modèle mais n'existe pas chez le pommier). Les valeurs prises sont celles de la variété alexandra.
    ins_ram = [{'nom_arbre': nom_arbre , 'nom_rameau': rameau[0]  , 'date': date , 'tl_masse_seche': rameau[1], 'f2_concent_sorbitol': valeurs_sucres[0] , 'f2_concent_sucrose': valeurs_sucres[1] , 'f2_concent_glucose': valeurs_sucres[2] , 'f2_concent_fructose': valeurs_sucres[3] , 'f2_nombre_unites': rameau[2] , 'f2_masse_seche': rameau[3] , 'pf1_nombre_unites': rameau[4] , 'pf1_masse_seche': rameau[5], 'pf2_nombre_unites': rameau[6] , 'pf2_masse_seche': rameau[7], 'pf3_nombre_unites': rameau[8] , 'pf3_masse_seche': rameau[9], 'f2_tms_pulpe': rameau[11]}for rameau in rameauxmixte]
    sql += insert_into("rameauxmixte",header,ins_ram)
    return sql


#===========================================================#


def tree_csv(nom_arbre, date, variete, vr_masse_seche, jr_masse_seche, vb_masse_seche, architecture,rameauxmixte):
    #table "architecture" (géométrie rammeaux mixte + vieux bois)
    header = ['index','nom_arbre','niveau', 'nom_rameau', 'annee', 'diametre_base', 'diametre_ext', 'metamere', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'longueur']
    ins_architecture = [{'index': rameau[12],'nom_arbre':nom_arbre,'niveau':rameau[0], 'nom_rameau':rameau[1], 'annee':int(date.split("-")[0]), 'diametre_base': rameau[2], 'diametre_ext' : rameau[3], 'metamere' : rameau[4], 'x1' :rameau[5], 'y1':rameau[6], 'z1':rameau[7], 'x2':rameau[8], 'y2':rameau[9], 'z2':rameau[10], 'longueur':rameau[11]} for rameau in architecture]
    save_csv(header,ins_architecture,nom_arbre + "_architecture.csv")
    
    #table "rameauxmixte" (matière sèche, concentration en sucres, nombre de pousses feuillées et de fruits...).
    header = ['index','nom_arbre', 'nom_rameau', 'date', 'tl_masse_seche', 'f2_tms_pulpe', 'f2_concent_sorbitol', 'f2_concent_sucrose', 'f2_concent_glucose', 'f2_concent_fructose', 'f2_nombre_unites', 'f2_masse_seche', 'pf1_nombre_unites', 'pf1_masse_seche', 'pf2_nombre_unites', 'pf2_masse_seche', 'pf3_nombre_unites', 'pf3_masse_seche']
    valeurs_sucres = (0.0018, 0.0104, 0.0185, 0.0182)#Valeurs "bidon" de teneur en sucre des fruits (nécessaire pour le modèle mais n'existe pas chez le pommier). Les valeurs prises sont celles de la variété alexandra.
    ins_ram = [{'index': rameau[10],'nom_arbre': nom_arbre , 'nom_rameau': rameau[0]  , 'date': date , 'tl_masse_seche': rameau[1], 'f2_concent_sorbitol': valeurs_sucres[0] , 'f2_concent_sucrose': valeurs_sucres[1] , 'f2_concent_glucose': valeurs_sucres[2] , 'f2_concent_fructose': valeurs_sucres[3] , 'f2_nombre_unites': rameau[2] , 'f2_masse_seche': rameau[3], 'pf1_nombre_unites': rameau[4] , 'pf1_masse_seche': rameau[5], 'pf2_nombre_unites': rameau[6] , 'pf2_masse_seche': rameau[7], 'pf3_nombre_unites': rameau[8] , 'pf3_masse_seche': rameau[9], 'f2_tms_pulpe': rameau[11]} for rameau in rameauxmixte]
    save_csv(header,ins_ram,nom_arbre + "_rameauxmixtes.csv")

def quote_str(v):
    if type(v) == type(""):
        return "'"+v+"'"
    else:
        return str(v)

def insert_into(table, header, dict_list):
    """
        Renvoie une ligne de commande SQL "INSERT INTO"
        table (string) : la table sur laquelle faire l'insert
        dict_list (list of dict) : en clef le nom des champs de la table, en valeur leur valeur (si on insert une seule ligne) ou un tableau de valeurs (si on insert plusieurs lignes en une commande)
    """
    values = ["(" + ",".join([quote_str(dict[key]) for key in header]) + ")" for dict in dict_list]
    return "INSERT INTO " + table + " ("+",".join(header)+") VALUES\n"+",\n".join(values)+";\n"

def save_csv(header,dict_list,filename):
    values = [";".join([str(dict[key]) for key in header]) for dict in dict_list]
    f=open(filename,'w')
    f.write(";".join(header)+"\n"+"\n".join(values))
    f.close()

import random

def extract_architecture(mtg_file_path,nom_arbre,date,variete,SLA,densite_MS_rameaux,TMS_fruits,SR,charge_fruits=None,seed=None):
    '''
    Converti un fichier .mtg généré par MAppleT en une architecure au format Qualitree. Le script .sql est renvoyé en sorti de cette fonction (il faudra l'enregistrer dans un fichier),
    des fichiers .csv correspondants aux tables de la bdd Qualitree sont aussi générés (cela permet de visualiser le résultat plus facilement qu'en SQL).

    mtg_file : chemin vers le .mtg que l'on souhaite convertir.
    nom_arbre : le nom à donner à l'architecture dans la base de données de qualitree.
    date : date à indiquer dans la base de données de qualitree (date de début de simulation)
    variete : variété, tel que notée dans le fichier parametres.xml
    SLA : specific leaf area
    densite_MS_rameaux : densité du bois en g.m-3
    TMS_fruits : teneur en matière sèche des fruits
    SR : shoot-root ratio utilisé pour calculer la masse des jeunes ou vieilles racines en fonction de celle des pousses feuillées ou du vieux bois+tiges de rameaux mixtes (respectivement)
    charge_fruits : par défaut les fruits sont ceux indiqués dans le .mtg. Si une valeur est indiquée (entre 0. et 1.), elle défini la proportion d'inflorescences portant un fruit (0.: pas de fruits, 1.: un fruit par inflorescence).  
    La masse des fruits quand la charge est fixée est égale à la moyenne de la masses des fruits dans le .mtg
    seed : graine du générateur de nombre pseudo aléatoire utilisé pour déterminer quelles inflorescences portent un fruit, par défaut la graine est aléatoire.
    '''
    m = MTG(mtg_file_path)
    plants = VtxList(Scale=1)
    
    annees = sorted(list(set([an(x) for x in uc(plants[0])])))

    ram_mixtes = list(set(rameaux(plants[0])))#rameaux mixtes

    #Les rameaux mixtes doivent être des UC de l'année précédente, sinon la condition de qualitree comme quoi un rameau mixte ne peut pas porter de ramifications n'est pas respectée, hors des bugs de MAppleT peuvent entrainer que certaines feuilles ne tombent pas ou que plusieurs UC soient produites dans la même année, les rameaux non conformes sont supprimés. 
    ram_mixtes_error = [x for x in ram_mixtes if an(x) != annees[-2]]
    for r in ram_mixtes_error:
        print 'ERREUR : rameaux mixte ' + Class(r) + str(Index(r)) +  ' avec pour année de croissance ' + str(an(r)) + '. Ce rameau ne sera pas considéré comme mixte'
        
    ram_mixtes = [x for x in ram_mixtes if an(x) == annees[-2]]

    rm = ram_mixtes
    while True:
        rm_new = list(set([Father(x) for x in rm] + rm))#On ajoutte le vieux bois
        if len(rm_new) == len(rm):#On s'arrête quand on ne trouve plus de nouveaux rameaux.
            break
        else:
            rm = rm_new
    rm = [x for x in rm if  x != None]

    names = qualitree_nom_rameaux(rm)

    '''Il faut renseigner la "longeur du métamère" pour chaque rameau dans la base de données.
    Cette valeur est la longeur en mm entre la ramification précédente et celle portant le rameau,
    sur le rameau parent.'''
    metameres_qualitree = {}
    chiffres = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for x in rm:
        if(Father(x)==None):#La "longueur du métamère" n'a pas de sens pour le tronc.
            metameres_qualitree[x] = 0#Qualitree demande que l'on indique 0.
        else:
            intervale = None
            father_mets = Components(Father(x)) #métamères du du père de x
            ramif_index = father_mets.index(Father(Components(x)[0])) #position du métamère (au sens de MAppleT) portant le rameau x sur le père de x.
            if names[x][-1]=="1":#Pour la première ramification d'un rameau, le métamère est sa distance avec le début du parent.
                intervale = father_mets[:ramif_index+1] #Liste des métamères dont la longueur doit etre comptée.
            else:#Pour les ramifications suivantes, on prends la longeur entre cette ramification et la précédente.
                nom_ramif_prec = names[x][:-1] + chiffres[chiffres.index(names[x][-1])-1]
                ramif_prec = [c for c,v in names.items() if v == nom_ramif_prec][0]
                index_ramif_prec = father_mets.index(Father(Components(ramif_prec)[0]))
                intervale = father_mets[index_ramif_prec+1:ramif_index+1]
            met = round(sum([length(m) for m in intervale])*1000,1)
            metameres_qualitree[x] = met if met != 0 else 1



    tab_architecture = []

    base_sous_sol = [x for x in rm if zz(Components(x)[0]) <= 0]
    sommet_sous_sol = [x for x in rm if zz(Components(x)[-1]) <= 0]
    for r in base_sous_sol:
        print 'ERREUR : la base de l\'UC ' + Class(r) + str(Index(r)) + ' est sous le plan horizontal, Y1 sera fixé à 0.1'

    for r in sommet_sous_sol:
        print 'ERREUR : le sommet de l\'UC ' + Class(r) + str(Index(r)) + ' est sous le plan horizontal, Y2 sera fixé à 0.1'

    tab_architecture += [[
             niveau(names[x]),#Order(x),#marche pas?
             names[x],
             topdia(Components(x)[0]),#diametre_base
             topdia(Components(x)[-1]),#diametre_ext
             metameres_qualitree[x],#metameres
             round(xx(Components(x)[0])*1000,1),round((zz(Components(x)[0]) if (zz(Components(x)[0]) > 0.0) else 0.0001)*1000,1),round(-yy(Components(x)[0])*1000,1),#x1, y1, z1 #Conversion repère MappleT (m) à reprère Qualitree (q) : Xq=Xm Yq=Zm Zq=-Ym, conversion m -> mm. On s'assure que Y > 0 sinon on le fixe à 0 (condition qualitree).
             round(xx(Components(x)[-1])*1000,1),round((zz(Components(x)[-1]) if zz(Components(x)[-1]) > 0.0 else 0.0001)*1000,1),round(-yy(Components(x)[-1])*1000,1),
             round(length_uc(x)*1000,1),
             Class(x) + str(Index(x)),
            ]for x in rm]
    #save(tab_architecture,'test.csv')

    if charge_fruits == None:
        tab_rameauxmixte = [[names[x],
                             vol_uc(x)*densite_MS_rameaux,
                             fruit_ram(x),
                             fruit_ram_ms(x),
                             nb_leafy_rameau_cat(x, 'small'),
                             la_rameau_cat(x, 'small')/SLA + vol_rameau_cat(x, 'small')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                             nb_leafy_rameau_cat(x, 'medium'),
                             la_rameau_cat(x, 'medium')/SLA + vol_rameau_cat(x, 'medium')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                             nb_leafy_rameau_cat(x, 'large'),
                             la_rameau_cat(x, 'large')/SLA + vol_rameau_cat(x, 'large')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                             Index(x),
                             TMS_fruits,
                           ]for x in ram_mixtes]
        #save(tab_rameauxmixte,'test2.csv')
    else:
        charge_fruits = float(charge_fruits)
        assert(0. <= charge_fruits and charge_fruits <= 1.)
        if seed != None:
            random.seed(seed)
        ms_moy_fruit = float(sum([fruit_ram_ms(x) for x in ram_mixtes]))/sum([fruit_ram(x) for x in ram_mixtes])
        nb_I =  [len([y for y in Sons(x) if Class(y) == "I"]) for x in ram_mixtes]
        nb_F = int(round(sum(nb_I) * charge_fruits))

        inflos = []
        for x,i in zip(ram_mixtes,nb_I):
            inflos += [x]*i
        random.shuffle(inflos)
        inflos = inflos[0:nb_F]#On choisi au hasard les inflorescences portant un fruit.
        ram_mixte_nb_F = {x:inflos.count(x) for x in ram_mixtes} 

        tab_rameauxmixte = [[names[x],
                        vol_uc(x)*densite_MS_rameaux,
                        ram_mixte_nb_F[x],
                        ram_mixte_nb_F[x]*ms_moy_fruit,
                        nb_leafy_rameau_cat(x, 'small'),
                        la_rameau_cat(x, 'small')/SLA + vol_rameau_cat(x, 'small')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                        nb_leafy_rameau_cat(x, 'medium'),
                        la_rameau_cat(x, 'medium')/SLA + vol_rameau_cat(x, 'medium')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                        nb_leafy_rameau_cat(x, 'large'),
                        la_rameau_cat(x, 'large')/SLA + vol_rameau_cat(x, 'large')*densite_MS_rameaux,#MS feuilles + tiges des pousses feuillées
                        Index(x),
                        TMS_fruits,
                    ]for x in ram_mixtes]




    vb_masse_seche = sum([vol_uc(x)*densite_MS_rameaux for x in rm if not x in ram_mixtes])
    vb_masse_seche = vb_masse_seche if vb_masse_seche != None else 0#Pour les arbres jeunes (sans vieux bois), sum([]) = None
    vr_masse_seche = sum([vol_uc(x)*densite_MS_rameaux for x in rm])/SR #La masse sèche de vieilles racines est calculée en fonction de la masse des UC en croissance secondaire (vieux bois+tiges de rameaux mixte) et du shoot-root ratio.
    jr_masse_seche = sum([la_rameaux(x)/SLA + sum([vol_uc(y) for y in Sons(x)])*densite_MS_rameaux for x in ram_mixtes])/SR #La masse sèche des jeunes racines est calculée en fonction de la masse des pousses feuillées (tige+feuilles) et du shoot-root ratio.

    tree_csv(nom_arbre,date,variete,vr_masse_seche, jr_masse_seche, vb_masse_seche,tab_architecture,tab_rameauxmixte)
    del m
    return tree_sql(nom_arbre,date,variete,vr_masse_seche, jr_masse_seche, vb_masse_seche,tab_architecture,tab_rameauxmixte)

def qualitree_nom_rameaux(rmx):
    """ Défini le nom des rameaux qualitree
    rmx (list of vtx) : liste des rameaux mixtes et du vieux bois.
    Renvoie un dictionaire avec comme clef l'id du vtx et comme valeur le nom Qualitree"""
    
    chiffres = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    fathers = [Father(x) for x in rmx]
    qnames = {rmx[fathers.index(None)]:'r0'}#le tronc n'a pas de pêre.
    rmx2 = [rmx[fathers.index(None)]] #rameaux dont on a déterminé le nom qualitree mais pas celui de ses enfants
    while len(rmx2) > 0:
        vtx = rmx2[0]#le rameau sur lequel on travaille
        childrens = [rmx[i] for i,x in enumerate(fathers) if x == vtx]#On récupère tous les enfants présents dans rmx (les autres enfants comme les pousses feuillées sont exclus)
        
        rmx2 = rmx2[1:]#On retire le rameau de la liste des rameaux dont il faut déterminer le nom des enfants
        rmx2 += childrens #On rajoutte les enfants dans la liste
        
        if len(childrens)>0:#Si le rameau a des enfants on les nomme
            vtx_metamers = Components(vtx)
            childrens_metamer_position = [vtx_metamers.index(Father(Components(x)[0])) for x in childrens]#position du pêre des enfants dans vtx (à l'échelle du métamère)
            sorted_metamer_position = sorted(childrens_metamer_position)
            childrens_position = [sorted_metamer_position.index(x)+1 for x in childrens_metamer_position] #position des enfants entre eux (1 pour le premier, 2 pour le deuxième...).
            
            c_p=[]
            for i in childrens_position:#Si il y a des doublons dans childrens_position on incrémente l'un d'entre eux (quand eux rameaux partent du même métamère)
                if i not in c_p:
                    c_p.append(i)
                else:
                    c_p.append(i+1)
            childrens_position=c_p

            if qnames[vtx]=='r0':#les fils du tronc sont nommées r1, r2, r3...
                for k in range(len(childrens)):
                    assert childrens_position[k] <= len(chiffres), 'Le rameau r0 a {rams} ramifications, ce qui est supérieur au nombre maximal de {max}'.format(rams=childrens_position[k],max=len(chiffres))
                    qnames[childrens[k]]='r'+str(chiffres[childrens_position[k]-1])
            else:#sinon ils ont le nom du père suivi de -0, -1, -2...
                for k in range(len(childrens)):
                    qnames[childrens[k]]=qnames[vtx]+'-'+str(chiffres[childrens_position[k]-1])



    return qnames

def niveau(name):
    return 0 if name == 'r0' else name.count('-')+1



