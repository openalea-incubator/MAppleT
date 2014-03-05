from openalea.lpy import *
__revision__ = " $Id: stocatree.lpy 9964 2010-11-23 12:24:26Z cokelaer $ "
try:
    import openalea.stocatre.optimisation as optimisation
except:
    import openalea.stocatree.non_optimised as optimisation
import openalea.stocatree.constants as constants
from openalea.stocatree.output import Data
from openalea.stocatree.colors import Colors
from openalea.stocatree.tree import Tree
from openalea.stocatree.leaf import AppleLeaf
from openalea.stocatree.fruit import AppleFruit
from openalea.stocatree.wood import Wood
from openalea.stocatree.internode import Internode
from openalea.stocatree.apex import apex_data
from openalea.plantik.tools.config import ConfigParams
from openalea.stocatree.tools.simulation import SimulationStocatree
from openalea.stocatree.sequences import Markov, generate_sequence, terminal_fate
from openalea.stocatree.metamer import metamer_data
from openalea.stocatree.growth_unit import growth_unit_data
from openalea.sequence_analysis import HiddenSemiMarkov
from vplants.plantgl.all import Vector3, cross, Viewer
from openalea.stocatree.srandom import boolean_event
from openalea.stocatree.physics import rotate_frame_at_branch, rupture
from openalea.stocatree.tools.surface import *
from openalea.stocatree import get_shared_data

import time
import os
import datetime

gravity = Vector3(0.0, 0.0, -9.81);  #// in m s^-2 original mappleT

# First, read the configuration file
options = ConfigParams(get_shared_data('stocatree.ini'))

# Then, define a data structure to store outputs such as MTG, counts, sequences and so on
data = Data(options=options, revision=__revision__)

# Initialise the simulation
simulation = SimulationStocatree(dt=options.general.time_step, 
  starting_date=options.general.starting_year, 
  ending_date=options.general.end_year)

# Read PGLshape surfaces
stride = int(options.stocatree.stride_number)
leaf_surface = leafSurface(stride, stride)
ground_surface = groundSurface(stride, stride)
petal_surface = petalSurface(stride, stride)

# init markov and tree instances
markov          = Markov(**options.markov.__dict__)
markov.hsm_96_medium = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y3_96.txt'))
markov.hsm_97_medium = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y4_97.txt'))
markov.hsm_98_medium = HiddenSemiMarkov(get_shared_data('fmodel_fuji_5_15_y5_98.txt'))
markov.hsm_95_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_y12.txt'))
markov.hsm_96_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_16_65_y3_96.txt'))
markov.hsm_97_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_16_65_y4_97.txt'))
markov.hsm_98_long = HiddenSemiMarkov(get_shared_data('fmodel_fuji_16_65_y5_98.txt'))

# The following objects (tree, wood, internode, apex_parameters, leaf, fruit
# are used to store the user parameters and are used by the metamer_data 
# class to create new metamers.
# 
# tree is unique throughout the simulation, so only one instance is used
tree            = Tree(**options.tree.__dict__)
# wood and internode are unique as well isnce they only contain parameters
wood            = Wood(**options.wood.__dict__)
internode       = Internode(**options.internode.__dict__)

#!!! apices and leaves are specific to a metamer later on a deepcopy is used.

temp = {}
temp.update(options.apex.__dict__)
temp.update(options.markov.__dict__)
apex_parameters = temp
leaf_parameters = options.leaf.__dict__
fruit_parameters = options.fruit.__dict__

# setup the colors once for all
colors = Colors()

#define the leaf area function once for all
simulation.func_leaf_area_init(get_shared_data('functions.fset'))


###################################
# DONT CHANGE ANYTHING HERE BELOW #
###################################

#define the group enumerate here 0 used for rendering. !! physics and update_parameters inverse on purpose
initialisation    = 0
update_parameters = 1
update_structure  = 4
statistics        = 3
physics           = 2

# module apex(apex_data): scale=2
# module branch(): scale=1
# module growth_unit(growth_unit_data): scale=1
# module axiom()
# module metamer(metamer_data): scale=2
# module root(): scale=1

numerical_resolution_counter = 0

def Start():
    global time1
    time1 = time.time()
    #random.seed(simulation.seed)
    # init the data to store the required outputs (sequence, lstring, mtg, ...)
    data.init()

def StartEach():
    if simulation.date.year in [1994,1995]:
        markov.hsm_medium = markov.hsm_96_medium
        markov.hsm_long   = markov.hsm_95_long
    elif simulation.date.year == 1996:
        markov.hsm_medium = markov.hsm_96_medium
        markov.hsm_long   = markov.hsm_96_long
    elif simulation.date.year == 1997:
        markov.hsm_medium = markov.hsm_97_medium
        markov.hsm_long   = markov.hsm_97_long
    else:
        markov.hsm_medium = markov.hsm_98_medium
        markov.hsm_long   = markov.hsm_98_long


def EndEach(lstring):
    global time1

    if (simulation.date.month==1 and simulation.date.day == 1) or (simulation.date.month==6 and simulation.date.day==30) and simulation.phase == physics:
       print simulation.date, time.time()-time1, len(lstring)

    if simulation.date > simulation.ending_date:
        print 'The simulation has ended  %s %s\n' %  (options.general.end_year, simulation.date)
        Stop()
        End(lstring)
    # This switch controls the selection of which group of
    # productions to apply.  The general sequence is:
    #  initialisation --> update parameters --> output (L-string or MTG) --> physics --> statistics --> update structure --> update parameters
    # Rendering happens after 'update parameters'.  'output' is only
    # called conditionally; mostly, the simulation goes straight from
    # 'output parameters' to 'physics'
    
    if simulation.phase == initialisation:
        useGroup(update_parameters)
        simulation.phase = update_parameters
        frameDisplay(False)
    elif simulation.phase == update_parameters:
        global numerical_resolution_counter
        numerical_resolution_counter += 1
        if numerical_resolution_counter < simulation.rotation_convergence.steps:
            simulation.dt = 0.0 # days
            frameDisplay(False)
            #jump to the physics phase
        else:
            if options.general.verbose is True:
                print '%s (n elts=%s, it=%s)' % (simulation.date, len(lstring), getIterationNb())
            if options.stocatree.saveimage is True:
                print 'saving stocatree_output%05d.png' % getIterationNb(), 'png'
                Viewer.frameGL.saveImage('stocatree_output%05d.png' % getIterationNb(), 'png')

            simulation.dt = simulation.base_dt
            numerical_resolution_counter = 0

        newyear = simulation.advance()
        #TODO#

        if simulation.events.harvest.active:
            tree.fruits_harvested = tree.fruits 
            tree.fruits = 0
            simulation.harvested = True

        #outputs
        if options.output.mtg:
            save = data.mtg.advance(simulation.dt)
            if save:
                data.mtg.build_filename("%4.0f_%02d_%02d" % (simulation.date.year, simulation.date.month, simulation.date.day))
                data.mtg.init()
                data.mtg.save(lstring, simulation.date, tree.trunk_radius)

        # save trunk data
        if options.output.trunk:
            data.trunk.save(simulation.date, tree.trunk_radius,tree.trunk_cross_sectional_area)

        # save the lstring
        if options.output.l_string:
            save = data.l_string.advance(simulation.dt)
            if save:
                data.l_string.save(lstring, simulation.date)

        # save the shoot counts
        if options.output.counts:
            save = data.counts.advance(simulation.dt)
            if save:
                data.counts.save(simulation.date)
            if simulation.date.day == 0:
                data.counts.reset()
        
        useGroup(physics)
        simulation.phase = physics
        backward()
    elif simulation.phase == statistics:
        useGroup(update_structure)
        simulation.phase = update_structure
        frameDisplay(False)
    elif simulation.phase == physics:
        useGroup(statistics)
        simulation.phase = statistics
        forward()
        frameDisplay(False)
    elif simulation.phase == update_structure:
        useGroup(update_parameters)
        simulation.phase = update_parameters
        frameDisplay(False) 
    else:
        ValueError('must not enter here')



def End(lstring):

    global data
    data.close_all()
    data.save()
    global time1

    if options.stocatree.savescene is True:
        s = Viewer.getCurrentScene()
        s.save('stocatree.bgeom')
        s.save('stocatree.pov')
    
    time2 = time.time()
    print 'Elpsed time:',time2-time1
    print 'Final iteration nb',getIterationNb()
    print '%s (n elts=%s, it=%s)' % (simulation.date, len(lstring), getIterationNb())

    if options.stocatree.movie is True:
        from openalea.plantik.tools.movies import create_movie
        create_movie(input_glob='stocatree*png', output_filename='stocatree')


__derivation_length__ =  int(options.general.max_iterations)

__axiom__ = [75]

# ignore: growth_unit

# production:

# The L-system starts with this group.  If there were any errors
# in the initialisations in Start, pruduce an error message;
# otherwise, start the simulation.
# group 0:

def __p_0_0_axiom() :
    a = apex_data(tree.initial_hlu, 'trunk', **apex_parameters)
    return pproduce(0,a)


# Update the parameters of each metamer (age, reaction wood,
# organs, length, rigidity & shape memory) and perform the
# geometric reconstruction (rotation and placement of each metamer)
# group 1:

def __p_1_0_metamer_ml_branchmetamer_m_(ml,m) :
    m.update_metamer_parameters(simulation)
    m.organ_activity(simulation)
    if options.stocatree.mechanics:
        m.hlu = rotate_frame_at_branch(ml.hlu, ml.branching_angle,  ml.phyllotactic_angle);
        m.hlu = optimisation.reorient_frame(m.hlu, m.rotation_velocity, m.length)
    m.update_position(ml.position)
    return pproduce(1,m)

def __p_1_1_metamer_ml_metamer_m_(ml,m) :
    m.update_metamer_parameters(simulation)
    m.organ_activity(simulation)
    if options.stocatree.mechanics:
        m.hlu = optimisation.reorient_frame(ml.hlu, m.rotation_velocity, m.length)
    m.update_position(ml.position)
    return pproduce(2,m)

def __p_1_2_metamer_m_(m) :
    m.update_metamer_parameters(simulation)
    m.organ_activity(simulation)
    m.update_position()
    return pproduce(3,m)
#X:
#  produce Cut()


# Calculate the width (by the pipe model), cumulated mass, cumulated torque and
# rotation velocity of each metamer
#group physics
# group 2:

def __p_2_0_rootmetamer_m_(m) :
    tree.trunk_radius = m.radius
    tree.trunk_cross_sectional_area = constants.pi * m.radius * m.radius
    tree.fruit_load = tree.fruits / tree.trunk_cross_sectional_area

def __p_2_1_metamer_m__branchmetamer_mb__metamer_mr_(m,mb,mr) :
    radius = optimisation.get_new_radius(mb.radius, mr.radius)
    if m.leaf.state=='growing':
        radius = optimisation.get_new_radius(radius, m.leaf.petiole_radius)
    m.radius = optimisation.max(radius, m.radius);
    #update last layer thickness
    m.layers[-1].thickness = m.radius - m.layers[-1].radius
    m.compute_mass(mr, mb)
    #cumulated torque cumulate mass must be in kg
    if options.stocatree.mechanics:
        m.cumulated_torque =  mb.cumulated_torque + mr.cumulated_torque + \
           cross((mb.hlu.heading * mb.length), (gravity * mb.cumulated_mass)) \
           + cross((mr.hlu.heading * mr.length), (gravity * mr.cumulated_mass))\
           + cross((m.hlu.heading * m.length) , tree.tropism)
        m.calculate_rotation_velocity(simulation, options.stocatree.stake)
    return pproduce(4,m)

def __p_2_2_metamer_m_metamer_mr_(m,mr) :
    radius = mr.radius
    if m.leaf.state == 'growing':
        radius = optimisation.get_new_radius(mr.radius, m.leaf.petiole_radius)
    m.radius = optimisation.max(radius, m.radius)
    m.layers[-1].thickness = m.radius - m.layers[-1].radius
    m.compute_mass(mr)
    if options.stocatree.mechanics:
        m.cumulated_torque \
            = cross((mr.hlu.heading * mr.length), (gravity * mr.cumulated_mass))\
            + mr.cumulated_torque \
            + cross((m.hlu.heading * m.length) , tree.tropism)
        m.calculate_rotation_velocity(simulation, options.stocatree.stake)
    return pproduce(5,m)

def __p_2_3_metamer_m_apex_a_(m,a) :
    # wood.density, m.fruit_mass  aer units objects
    radius = a.radius
    if m.leaf.state=='growing':
        radius = optimisation.get_new_radius(a.radius, m.leaf.petiole_radius)
    m.radius = optimisation.max(radius, m.radius);
    m.layers[-1].thickness = m.radius - m.layers[-1].radius
    m.compute_mass()
    m.cumulated_torque = cross( m.hlu.heading * m.length , tree.tropism)    
    if options.stocatree.mechanics:
        m.calculate_rotation_velocity(simulation, options.stocatree.stake)
    return pproduce(6,m)

def __p_2_4_apex_a_(a) :
    if (a.sequence_position == 0 and a.radius < a.target_radius):
        a.terminal_expansion(simulation.dt.days)
    return pproduce(7,a)
#X:
#  produce Cut()

#// Generate new sequences
#group statistics
# group 3:

def __p_3_0_apex_a_(a) :
    
    #fprint simulation.events.bud_break
    
    if (a.sequence_position == 0 and a.get_observation()!='dormant' and
      (a.parent_observation == 'floral' or simulation.events.bud_break.active)):
        
        old_observation = a.get_observation()
        a.sequence  = generate_sequence(a.get_observation(),\
            markov, simulation.date.year, options.stocatree.second_year_draws,
            select_trunk=[int(options.stocatree.select_trunk)])
        a.sequence_position = len(a.sequence)
        if (a.get_observation()=='trunk'):
            a.set_observation('large')
        elif (a.get_observation()=='small' and boolean_event(tree.spur_death_probability)):
            a.set_observation('dormant')
        elif (a.get_observation()=='floral'):
            a.set_observation('dormant')
        else:
            a.set_observation(terminal_fate(simulation.date.year,a.get_observation()))
        a.parent_observation = old_observation
        a.radius = 0
        a.max_terminal_radius_target();
        #CHANGES tree.growth_units
        tree.growth_units += 1
        #update counts
        if options.output.counts:
            if a.parent_observation=='floral':
                data.counts.florals+=1
            elif a.parent_observation == 'small':
                data.counts.shorts+=1
            elif a.parent_observation == 'medium':
                data.counts.mediums+=1
            elif a.parent_observation == 'large':
                data.counts.longs += 1
                if (a.sequence_position < 26):
                    data.counts.len_16_to_25 +=1
                elif (a.sequence_position < 41):
                    data.counts.len_26_to_40+=1
                else:
                    data.counts.len_over_40+=1
        # save sequences into output data
        if (options.output.sequences and simulation.date.year < 1999 and (a.parent_observation in ['large','medium','small'])):
            data.sequences.save(a.sequence, a.sequence_position)
        pproduce(8,growth_unit_data(tree.growth_units, simulation.date.year, a.parent_observation == 'floral'),a)
    else:
        return pproduce(9,a)
#X:
#  produce Cut()


#// Add new apices (terminal and lateral) and metamers
#// to the structure
#group update_structure
# group 4:


def __p_4_0_metamer_m_apex_a_(m,a) :
    # if plastochron is reached, we produce a new metamer
    if (a.sequence_position > 0 and m.age >= m.internode._plastochron):
        a.sequence_position-=1
        flower = (a.sequence_position == 0 and a.parent_observation=='floral')
        if m.year == simulation.date.year:
            number = m.number + 1
        else:
            number = 1
        #print fruit_parameters
        mn = metamer_data(floral=flower, number=number, hlu=a.hlu, 
          zone=a.sequence[a.sequence_position][0], observation=a.get_observation_from_sequence(),
                      p_angle=(m.phyllotactic_angle + tree.phyllotactic_angle),
                      b_angle=tree.branching_angle, wood=wood, internode=internode,
                      fruit=AppleFruit(**fruit_parameters), leaf=AppleLeaf(**leaf_parameters))
        mn.trunk = a.trunk;
        mn.year = simulation.date.year
        return pproduce(10,mn,a)
    else:
        return pproduce(11,a)


def __p_4_1_apex_a_(a) :
    #if Debug:print 'APEX seq pos=',a.sequence_position
    if (a.sequence_position > 0):
        a.sequence_position -= 1
        branching_angle = tree.branching_angle;
        flower = (a.sequence_position == 0 and a.parent_observation=='floral')
        #TODO check first and second index of a.sequence versus lsystem.l code
        m = metamer_data(floral=flower, number=1, hlu=a.hlu, zone=a.sequence[a.sequence_position][0], observation=a.get_observation_from_sequence(), p_angle=(tree.phyllotactic_angle), b_angle=branching_angle, wood=wood, internode=internode, 
                              fruit=AppleFruit(**fruit_parameters), leaf=AppleLeaf(**leaf_parameters))
        m.trunk = a.trunk
        m.year = simulation.date.year
        return pproduce(12,m,a)
    else:
        return pproduce(13,a)

def __p_4_2_metamer_m_metamer___apex_a_(m,a) :
    # case of a floral immediate lateral axis: should be treated as
    # laterals and not as terminals
    if (not m.developped and a.parent_observation == 'floral' and a.sequence_position == 0):
        m.developped = True
        if (boolean_event(tree.inflorescence_death_probability)):
            return pproduce(14,m)
        m.branching_angle = tree.floral_branching_angle
        hlu = rotate_frame_at_branch(m.hlu, m.branching_angle, m.phyllotactic_angle);
        sylleptic_apex = apex_data(hlu, terminal_fate(simulation.date.year, 'floral'), **apex_parameters)
        sylleptic_apex.parent_observation = 'floral'
        return pproduce(15,m,sylleptic_apex)

def __p_4_3_metamer_m_(m) :
    if (options.stocatree.ruptures and rupture(m.cumulated_torque, m.radius, wood._modulus_of_rupture)):
        print 'EXTRAORDINARY EVENT: There was a rupture in the system.\n'
        return pproduce(16,'Cut')
    if (m.observation!= 'dormant' and  not m.developped and simulation.events.bud_break.active):
        m.developped = True
        hlu = rotate_frame_at_branch(m.hlu, m.branching_angle, m.phyllotactic_angle)
        a = apex_data(hlu, m.observation, **apex_parameters)
        return pproduce(17,m,a)
    else:
        return pproduce(18,m)


#X:
#  produce Cut()

# group 0:
#// Graphical rendering of the tree
# interpretation:

def __h_0_0_root() :
    return pproduce(19,colors.ground,ground_surface)

def __h_0_1_metamer_m_(m) :
    #print 'interpretation called', getIterationNb()
    shoot_colour = colors.error
    if options.stocatree.render_mode == 'bark':
        shoot_colour = colors.bark
    elif options.stocatree.render_mode == 'observations':
        shoot_colour = colors.observation.get_color(m.observation)
    elif options.stocatree.render_mode == 'zones':
        shoot_colour = colors.zone.get_color(m.zone)
    elif options.stocatree.render_mode == 'reaction_wood':
        shoot_colour = colors.reaction_wood.get_color(m.layers[-1].reaction_wood)
    elif options.stocatree.render_mode == 'year':
        shoot_colour = colors.year.get_color(m.year, options.general.starting_year)
    pproduce(20,m.hlu.heading.x,m.hlu.heading.y,m.hlu.heading.z,m.hlu.up.x,m.hlu.up.y,m.hlu.up.z)
    pproduce(21,m.radius*12.,shoot_colour,m.length*10)
    d2r = 180.0 / constants.pi
    if (m.fruit.state == 'flower'):
        #TODO the five flowers are at the same place !!
        scale = 5.
        pproduce(22,m.phyllotactic_angle * d2r)
        pproduce(23)
        pproduce(24,colors.stamen)
        pproduce(25,0.0025*scale)
        pproduce(26)
        pproduce(27)
        pproduce(28)
        pproduce(29)
        pproduce(30)
        pproduce(31)
        pproduce(32)
        pproduce(33)
        pproduce(34)
        pproduce(35)
        pproduce(36)
        pproduce(37)
        pproduce(38,colors.petal)
        pproduce(39,petal_surface,0.02*scale)
        pproduce(40,petal_surface,0.02*scale)
        pproduce(41,petal_surface,0.02*scale)
        pproduce(42,petal_surface,0.02*scale)
        pproduce(43,petal_surface,0.02*scale)
        pproduce(44)
    #
    elif (m.fruit.state == 'fruit'):
        r = m.fruit.mass *1.5
        if r != 0:
            pproduce(45,float(m.phyllotactic_angle * d2r))
            pproduce(46,r,colors.fruit,r)
    #f
    if m.leaf.state=='growing':
        r = m.leaf.mass *1000.
        if r==0:
            r=0.1
        #check max total mass should be less than 0.66 grams
        if simulation.events.autumn.active is False:
            pproduce(47,colors.leaf)
        else:
            pproduce(48,colors.autumn_leaf)
        #Don't touch this!!! change the r value only
        # at least don't change the factors between F and PglShape (keep the 0.1 factor).
        #TODO take m radisu into account 
        #nproduce (RollL(m.phyllotactic_angle * d2r) Up(90.0) SetWidth(0.002) F(r *0.1) RollToVert() PglShape(leaf_surface, r) EB())
        pproduce(49,m.phyllotactic_angle * d2r,r *0.1,leaf_surface,r)
        #nproduce (RollL(m.phyllotactic_angle * d2r) Up(90.0) SetWidth(0.002) F(r *0.1) ~l(r) EB())
    return pproduce(50)

# endgroup
# homomorphism:

# endlsystem
