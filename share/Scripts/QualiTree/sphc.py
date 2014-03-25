#-*- encoding: Latin-1 -*-
def sphc_sql(nb_jours,num_scenario,phc,description="",demandeur=""):
   str = insert_into("description_collet", ["scenario","description","demandeur"], [{"scenario":num_scenario, "description":description, "demandeur":demandeur}])
   liste = []
   for jour in range(nb_jours):
       for heure in range(1,25):
           liste += [{"date":jour,"heure":heure,"scenario":num_scenario,"psi_x":phc(jour,heure)}]
   str += insert_into("scenario_collet",["date","heure","scenario","psi_x"],liste)           
   return str

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

def phc_constant(jour,heure):
    return -1.5

def f(x):
    assert(0<=x and x<=1)
    x = float(x)
    return 4*(1-x)*x

def phc_variable(jour, heure, H1 = 5., H2 =22., PHCmax = -0.4, PHCmin = -1.3):
    if heure <= H1 or heure >= H2:
        return PHCmax
    else :
        X = (heure - H1)/(H2 - H1)
        return (PHCmin-PHCmax)*f(X)+PHCmax

def phc_variable_saison(jour,heure, PHCmaxList, PHCminList,H1 = 6., H2= 12.,H3=13., H4=22.):
    
    if heure <= H1:
        return PHCmaxList[jour]
    elif heure >= H4:
        return PHCmaxList[jour+1]
    elif heure <= H2:
        X = (heure - H1)/(H2 - H1)/2.
        return (PHCminList[jour]-PHCmaxList[jour])*f(X)+PHCmaxList[jour]
    elif heure <= H3:
        return PHCminList[jour]
    else:
        X = (heure - H3)/(H4 - H3)/2.+0.5
        return (PHCminList[jour]-PHCmaxList[jour+1])*f(X)+PHCmaxList[jour+1]

def creerScenario(pathsql,pathcsv,pathscenario,description,num):
    PHCminList, PHCmaxList = zip(*[(float(x),float(y)) for x,y in [ligne.strip().replace(",",".").split(";") for ligne in open(pathscenario)][1:]])

    def phc_vs(jour, heure):
        return phc_variable_saison(jour,heure, PHCmaxList, PHCminList)

    F = open(pathsql,'w')
    F.write(sphc_sql(len(PHCminList)-1,num,phc_vs,description,"Olivier"))
    F.close()

    F2 = open(pathcsv,'w')
    for j in range(len(PHCminList)-1):
        for h in range(24):
            F2.write(str(h)+';'+str(phc_vs(j,h)).replace(".",",")+'\n')

creerScenario('sphc_non_stresse.sql','sphc_non_stresse.csv',"sphc_min_max_non_stresse.csv","pas de stress",103)
creerScenario('sphc_stress_modere.sql','sphc_stress_modere.csv',"sphc_min_max_stress_modere.csv","stress modere",104)
creerScenario('sphc_fort_stress.sql','sphc_fort_stress.csv',"sphc_min_max_fort_stress.csv","fort stress",105)