from openalea.stocatree.wood import Wood

def test_wood():
    wood = Wood()
    assert wood._density == 1000.
    assert wood._reaction_wood_rate == 0.5
    assert wood._reaction_wood_inertia_coefficient == 0.1
    assert wood._youngs_modulus == 1.1*1e9
    assert wood._modulus_of_rupture == 50e6

