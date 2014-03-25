from mtg_to_qualitree import extract_architecture

SLA_fuji = 0.01155              #m2.g-1
Specific_weight = 0.40 * 10**6  #g.m-3 Sources : rapport S. Benzing 1999
TMS_fruits_Fuji = 0.153         #Teneur en matiere seche des fruits au debut de la simulation, Sources : E. Costes, donnees experimentales. 
SR = 4.55                       #Shoot-root ratio servant a initialiser les masses seche de jeunes et vielles racines en fonction de celles, respectivement, des pousses feuillees et du vieux bois+tige rameau mixte.

File = open("myF0.sql","w")
File.write(extract_architecture(mtg_file_path = "F_0.mtg", nom_arbre = "F_0", date = "1998-05-15", variete = "Fuji", SLA = SLA_fuji, densite_MS_rameaux = Specific_weight, TMS_fruits = TMS_fruits_Fuji, SR = SR))
#Alexandra comme variete afin d'avoir le fichier de parametres deja fait pour les premiers tests.
File.close()
