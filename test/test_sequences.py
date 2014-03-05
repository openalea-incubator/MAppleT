from openalea.stocatree.sequences import *
from openalea.sequence_analysis import HiddenSemiMarkov
from openalea.stocatree import get_shared_data

def test_length_pool():
    print length_pool(1994)
    print length_pool(1995)
    print length_pool(1996)
    print length_pool(1997)
    print length_pool(1998)
    print length_pool(1999)

def test_terminal_fate():
    for year in range(1993, 2001, 1):
        for code in ['small','large','medium','floral']:
            index = terminal_fate(year, code)
            assert index in ['large','small','medium','floral']


def test_data_terminal_fate():
    d = DataTerminalFate()
    assert d.get_data_terminal_fate(1995, 'large') ==  d.get_data_terminal_fate(1995, 'large')
    assert d.get_data_terminal_fate(1995, 'medium') ==  d.get_data_terminal_fate(1995, 'medium')
    assert d.get_data_terminal_fate(1995, 'small') ==  d.get_data_terminal_fate(1995, 'small')
    assert d.get_data_terminal_fate(1995, 'floral') ==  d.get_data_terminal_fate(1995, 'floral')
    assert d.get_data_terminal_fate(1995, 'large') ==  [0.500, 0.167, 0.000, 0.333]
    d._check_probabilities()
    
    try:
        d.get_data_terminal_fate(1995, 'dummy')
        assert False
    except:
        assert True


def test_generate_trunk():
    for i in range(1,10):
        seq = generate_trunk()
        assert len(seq)==55 or len(seq)==59


def test_generate_random_draw_sequence():
    seq = _generate_random_draw_sequence()
    assert len(seq) in [46, 20, 49, 57, 39, 51, 48, 53, 62]

def test_floral():
    seq = generate_floral_sequence()
    assert len(seq)==4


def test_short():
    seq = generate_short_sequence()
    assert len(seq)==4


def test_generate_hsm_sequence():
    try:
        hsm = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y3_96.txt'))
    except:
        hsm = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y3_96.txt'))
    seq = generate_hsm_sequence(hsm)

    try:
        sm = [1,2,3]
        seq = generate_hsm_sequence(sm)
    except:
        pass

def test_generate_bounded_hsm_sequence():
    try:
        hsm = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y3_96.txt'))
    except:
        hsm = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y3_96.txt'))
    seq = generate_bounded_hsm_sequence(hsm, 10, 15)


def test_non_parametric_distribution():
    pdf = [0.25,0.25, 0.25, 0.25]
    for i in range(100):
        index = _non_parametric_distribution(pdf)
        assert index>=1 
        assert index<=4

    pdf = [1,1,1,1]
    try:
        index = _non_parametric_distribution(pdf)
        assert False
    except:
        assert True
def test_markov():
    markov = Markov()
    assert markov.max_sequence_length == 100

def test_generate_sequence():
    from openalea.sequence_analysis import HiddenSemiMarkov

    seq = [[0,0]] * 65
    markov = Markov()

    try:
        markov.hsm_97_medium = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y4_97.txt'))
        markov.hsm_97_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_16_65_y4_97.txt'))
    except:
        markov.hsm_97_medium = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y4_97.txt'))
        markov.hsm_97_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_16_65_y4_97.txt'))
    markov.hsm_medium = markov.hsm_97_medium
    markov.hsm_long   = markov.hsm_97_long

    generate_sequence('trunk',  markov)
    generate_sequence('small',  markov)
    generate_sequence('floral', markov)
    generate_sequence('medium',  markov)
    # probability used, so we need to be sure that internally, res=1,2,3 are called to test all the code.
    for i in range(1,100):
        generate_sequence('large',  markov)
    generate_sequence('large',  markov, second_year_draws=True, year=1995)
    

    try:
        generate_sequence('dummy')
        assert False
    except:
        assert True


