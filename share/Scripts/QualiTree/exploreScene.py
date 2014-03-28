 #!/usr/bin/python

#-------------------------------------------------------------------------------
# Name:         exploreScene
# Purpose:      A script to extract information from a PlantGL scene.
# Author:       Da Silva
# Created:      03/26/2014
# Copyright:    (c) Da Silva 2014
# Licence:      CeCill/LGPL
#-------------------------------------------------------------------------------

import openalea.plantgl.all as pgl

def computeBoundingShape(scene, shape='bellipsoid'):
  """
  Compute a bounding volume for the given `scene`.
  The `shape` of this volume can be one of these keyword 
  Note that the `pgl.fit` could deliver different shapes by using
  one of the following keyword instead of 'ellipsoid':
  EXTRUDEDHULL ; ASYMMETRICHULL ; EXTRUSION ; SPHERE ; ASPHERE ; BSPHERE
  CYLINDER ; ACYLINDER ; BCYLINDER ; ELLIPSOID ; BELLIPSOID2 ; AELLIPSOID
  BELLIPSOID ; AALIGNEDBOX ; BALIGNEDBOX ; BOX ; ABOX ; BBOX ; CONVEXHULL
  """
  
  gr= fruti.pgl.Group([ sh.geometry for sh in scene ])
  tglset = pgl.fit( shape, gr )
  #hull = pgl.Shape( tglSet, __Green )
  return tglset

def ellipseDesc(lps):
  """
  Function to extract the center, radii and rotations of a given ellipse
  A bounding ellipse is generated as a Translated(Rotated(Scaled(Sphere)))
  Hence the ellipse center is given by the translation and its radii by the scaling
  """

  if isinstance(lps, pgl.Translated):
    cx, cy, cz = lps.translation
  else:
    print"missing Translated from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"

  ori = lps.geometry

  if isinstance(ori, pgl.Oriented):
    rotMat = ori.transformation().getMatrix3()
    az, el, roll = rotMat.eulerAnglesZYX()
  else:
    print"missing Oriented from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"
    az = 0
  
  scal = ori.geometry

  if isinstance(scal, pgl.Scaled):
    scMat = scal.transformation().getMatrix()
    rx, ry, rz, rt = scMat.getDiagonal()
  else:
    print"missing Scaled from the bounding ellipse as a Translated(Rotated(Scaled(Sphere)))"
    rx=ry=rz=1
    

  return cx,cy,cz,rx,ry,rz, az
