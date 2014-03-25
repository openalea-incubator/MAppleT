#!/bin/bash

USER=root
PASSWORD=qualitree

NOMARBRE=Alexandra
ANNEE=1997

BDD=arbre_init
mysql -u $USER -p$PASSWORD $BDD < $BDD.arbre.sql
mysql -u $USER -p$PASSWORD $BDD < $BDD.architecture.sql
mysql -u $USER -p$PASSWORD $BDD < $BDD.rameauxmixte.sql

BDD=arbre_observe
mysql -u $USER -p$PASSWORD $BDD < $BDD.rameauxmixte.sql

BDD=climat
mysql -u $USER -p$PASSWORD $BDD < $BDD.station.sql
mysql -u $USER -p$PASSWORD $BDD < $BDD.donnees_h.sql

BDD=potentiels_hydriques
mysql -u $USER -p$PASSWORD $BDD < $BDD.scenario_collet.sql
mysql -u $USER -p$PASSWORD $BDD < $BDD.description_collet.sql
