from openalea.stocatree.apex import apex_data
from openalea.stocatree.sequences import generate_sequence, Markov

markov = Markov()


class test_apex_data():

    def __init__(self):
        from openalea.stocatree.physics import Frame
        #test different constructors
        self.apex = apex_data(observation='small')
        self.apex = apex_data()

    def test_observation(self):

        self.apex.get_observation()
        try:
            self.apex.set_observation('dummy')
            assert False
        except:
            assert True

    def test_sequence(self):
        self.apex.sequence  = generate_sequence(self.apex.get_observation(),  markov, 1995, False)

        self.apex.sequence[0][1] = 1
        self.apex.sequence[1][1] = 2
        self.apex.sequence[2][1] = 3
        self.apex.sequence[3][1] = 4
        self.apex.sequence[4][1] = 0
        for index, choice in enumerate(self.apex.sequence):
            self.apex.sequence_position = index
            observation = self.apex.get_observation_from_sequence()
            assert observation in ['floral','dormant','large','medium','small']

    def test_radius_target(self):
        self.apex.sequence_position = 15
        self.apex.max_terminal_radius_target()

    def test_terminal_expansion(self):
        self.apex.terminal_expansion(10)
