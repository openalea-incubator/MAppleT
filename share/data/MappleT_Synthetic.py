import numpy.random
import openalea.lpy as lpy
import openalea.plantik.tools.config

if __name__ == "__main__":

    confp = openalea.plantik.tools.config.ConfigParams(
        str("MAppleT_Synthetic.ini"))

    def update_configuration(section, var, value):
        confp.__dict__[section].__dict__[var] = value

    # can't be modified
    update_configuration('general', 'starting_year', "1994")
    update_configuration('general', 'end_year', "1996-09-01")

    #update_configuration('stocatree', 'trunk_seq', "sequences_Fuji_4_txt.seq")
    update_configuration('stocatree', 'trunk_seq',
                         "sequences_hybride_239_txt.seq")

    update_configuration('general',
                         'output_dir',
                         "/home/artzet_s/code/dataset/synthetic_MAppleT")

    f = confp.general.filename

    for i in range(239):
        print("{}/239".format(i))
        update_configuration('general',
                             'output_filename',
                             "synthetic_{}".format(i))

        update_configuration('general',
                             'seed',
                             numpy.random.randint(1, 999999))

        update_configuration('fruit',
                             'max_absolute_growth_rate',
                             numpy.random.uniform(0.0025, 0.0045))

        update_configuration('fruit',
                             'probability',
                             numpy.random.uniform(0.30, 0.90))

        # update_configuration('tree',
        #                      'branching_angle',
        #                      numpy.random.randint(35, 55))
        #
        # update_configuration('internode',
        #                      'max_length',
        #                      numpy.random.uniform(0.01, 0.05))

        # update_configuration('leaf',
        #                      'max_area',
        #                      numpy.random.uniform(0.001, 0.01))

        # update_configuration('fruit',
        #                      'probability',
        #                      numpy.random.uniform(0.1, 0.7))

        # update_configuration('stocatree',
        #                      'select_trunk',
        #                      numpy.random.randint(1, 239))
        #
        update_configuration('stocatree',
                             'select_trunk',
                             i)

        lsys = lpy.Lsystem(confp.general.filename,
                           {"options": confp})
        lsys.animate()

    print("\nend\n")
