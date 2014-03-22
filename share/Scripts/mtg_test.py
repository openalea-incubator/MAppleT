import unittest

from mtg_to_qualitree import *

m = MTG('F_0.mtg')
plants = VtxList(Scale=1)
tree = plants[0]

# Here's our "unit tests".
class ExplorMtgTests(unittest.TestCase):

  def test_uc(self):
    what = len(uc(tree))
    res = 808
    self.failUnless(what == res)

  def test_an(self):
    what = annees = sorted(list(set([an(x) for x in uc(tree)])))
    res = [1994, 1995, 1996, 1997, 1998]
    self.failUnless(what == res)

  def test_class_uc(self):
    what = [class_uc(x) for x in uc(tree)][21:42]
    res = [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1]
    self.failUnless(what == res)

  def test_metamer(self):
    what = metamer(tree)[210:242]
    res = [181, 182, 185, 186, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197, 198, 199, 200, 201, 202, 205, 206, 207, 208, 209, 210, 211, 217, 218, 229, 240, 257, 263]
    self.failUnless(what == res)
    
  def test_la(self):
    what = (la(154), la(4766))
    res = (None,0.0018)
    self.failUnless(what == res)

  def test_uc1_leafy(self):
    what = uc1_leafy(tree)[100:121]
    res = [1643, 1654, 1675, 1721, 1732, 1758, 1763, 1796, 1838, 1847, 1854, 1914, 1921, 1927, 1933, 1939, 1946, 1952, 1959, 1966, 1973]
    self.failUnless(what == res)

  def test_la_uc(self):
    what = (round(la_uc(517),4), round(la_uc(521),4))
    res = (0.0037, 0.0022)
    self.failUnless(what == res)

  def test_nb_leafy_rameau(self):
    what = [nb_leafy_rameau(828), nb_leafy_rameau_cat(828, 'small'), nb_leafy_rameau_cat(828, 'medium'), nb_leafy_rameau_cat(828, 'large'), nb_leafy_rameau(505), nb_leafy_rameau_cat(505,'small'), nb_leafy_rameau_cat(505, 'medium'), nb_leafy_rameau_cat(505, 'large')]
    res = [3,2,1,0,2,1,1,0]
    self.failUnless(what == res)

  def test_fruit_rameau(self):
    what =[fruit_ram(293), round(fruit_ram_ms(293),4),fruit_ram(720), round(fruit_ram_ms(720),4)] 
    res = [1,0.0002,3,0.0006]
    self.failUnless(what == res)

  def test_lengths(self):
    what = [round(length_pousse(833),4), round(length_pousse(841),4), round(lencumul_ram(828),4)]
    res = [0.0184, 0.0339, 0.0523]
    self.failUnless(what == res)
    

def main():
    unittest.main()

if __name__ == '__main__':
    main()
