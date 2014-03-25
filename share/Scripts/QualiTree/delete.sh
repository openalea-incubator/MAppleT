#!/bin/bash

USER=root
PASSWORD=qualitree

NOMARBRE=Alexandra
ANNEE=1997
NOM_STATION=STEFCE_AV
SCENARIO=0

BDD=arbre_init
echo "delete from arbre where nom_arbre='$NOMARBRE' and year(date)=$ANNEE" | mysql -u $USER -p$PASSWORD $BDD
echo "delete from architecture where nom_arbre='$NOMARBRE' and annee=$ANNEE" | mysql -u $USER -p$PASSWORD $BDD
echo "delete from rameauxmixte where nom_arbre='$NOMARBRE' and year(date)=$ANNEE" | mysql -u $USER -p$PASSWORD $BDD

BDD=arbre_observe
echo "delete from rameauxmixte where nom_arbre='$NOMARBRE' and year(date)=$ANNEE" | mysql -u $USER -p$PASSWORD $BDD

BDD=climat
echo "delete from station where nom='$NOM_STATION'" | mysql -u $USER -p$PASSWORD $BDD
echo "delete from donnees_h where nom_station='$NOM_STATION'" | mysql -u $USER -p$PASSWORD $BDD

BDD=potentiels_hydriques
echo "delete from scenario_collet where scenario=$SCENARIO" | mysql -u $USER -p$PASSWORD $BDD
echo "delete from description_collet where scenario=$SCENARIO" | mysql -u $USER -p$PASSWORD $BDD
