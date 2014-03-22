# -*- coding: utf-8 -*-
def length(x1,y1,z1,x2,y2,z2):
  return pow(pow(x1-x2,2)+pow(y1-y2,2)+pow(z1-z2,2),0.5)

data=(('arbretest', 0, 'r0', 1997, 40, 25, 50, 0, 0, 0, 0, 500, 0),
  ('arbretest', 1, 'r1', 1997, 20, 12, 50, 0, 150, 0, 200, 300, 0),
  ('arbretest', 1, 'r2', 1997, 20, 12, 50, 0, 300, 0, -200, 500, 0),
  ('arbretest', 1, 'r3', 1997, 20, 12, 50, 0, 500, 0, 0, 750, 0),
  ('arbretest', 2, 'r1-1', 1997, 10, 3, 50, 100, 250, 0, 100, 400, 50),
  ('arbretest', 2, 'r2-1', 1997, 10, 3, 50, -100, 400, 0, -100, 500, 100),
  ('arbretest', 2, 'r3-1', 1997, 10, 3, 50, 0, 600, 0, 150, 750, -100))
  
for r in data: 
  print 'UPDATE architecture SET longueur=' + str(length(r[7],r[8],r[9],r[10],r[11],r[12])) + ' WHERE nom_arbre="' + r[0] + '" AND nom_rameau="' + r[2] + '" AND annee=' + str(r[3]) + ';'