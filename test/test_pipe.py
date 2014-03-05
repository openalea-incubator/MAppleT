import openalea.stocatree.pipe as pipe
import openalea.stocatree.optimisation as optimisation


def test_pipe():
    r = pipe.get_new_radius(1.,0)
    assert r==1
    r = optimisation.get_new_radius(1.,0)
    assert r==1

