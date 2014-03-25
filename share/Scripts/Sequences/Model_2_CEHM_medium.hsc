HIDDEN_SEMI-MARKOV_CHAIN

3 STATES

INITIAL_PROBABILITIES
0.999821    0.00017922  0           

TRANSITION_PROBABILITIES
0           0.99999     1e-05       
0           0           1           
0           0           1           

# transient class: state 0
# transient class: state 1
# recurrent class: state 2 (absorbing state)

# probability of no-occurrence of state 0: 0.00017922

# time up to the first occurrence of state 0 distribution
# mean: 0   variance: 0   standard deviation: 0

# time up to the first occurrence of state 0 frequency distribution - sample size: 80
# mean: 0   variance: 0   standard deviation: 0

# probability of no-occurrence of state 1: 9.99821e-06

# time up to the first occurrence of state 1 distribution
# mean: 1.57419   variance: 0.464825   standard deviation: 0.68178

# time up to the first occurrence of state 1 frequency distribution - sample size: 80
# mean: 1.525   variance: 0.252532   standard deviation: 0.502525

# time up to the first occurrence of state 2 distribution
# mean: 6.81784   variance: 3.48697   standard deviation: 1.86734

# time up to the first occurrence of state 2 frequency distribution - sample size: 80
# mean: 6.825   variance: 2.95633   standard deviation: 1.7194

# probability of leaving state 0: 0.635135

# state 0 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 0 recurrence time frequency distribution - sample size: 42
# mean: 1   variance: 0   standard deviation: 0

# probability of leaving state 1: 0.190586

# state 1 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 1 recurrence time frequency distribution - sample size: 344
# mean: 1   variance: 0   standard deviation: 0

# state 2 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 2 recurrence time frequency distribution - sample size: 240
# mean: 1   variance: 0   standard deviation: 0

STATE 0 OCCUPANCY_DISTRIBUTION
BINOMIAL   INF_BOUND : 1   SUP_BOUND : 4   PROBABILITY : 0.191489
# mean: 1.57447   variance: 0.464464   standard deviation: 0.681516
# coefficient of skewness: 0.905366   coefficient of kurtosis: 0.153021
# coefficient of variation: 0.432855

# state 0 sojourn time frequency distribution - sample size: 80
# mean: 1.525   variance: 0.252532   standard deviation: 0.502525

# final run - state 0 sojourn time frequency distribution - sample size: 0

STATE 1 OCCUPANCY_DISTRIBUTION
BINOMIAL   INF_BOUND : 1   SUP_BOUND : 16   PROBABILITY : 0.283132
# mean: 5.24698   variance: 3.04452   standard deviation: 1.74486
# coefficient of skewness: 0.24858   coefficient of kurtosis: -0.0715414
# coefficient of variation: 0.332545

# state 1 sojourn time frequency distribution - sample size: 80
# mean: 5.3   variance: 2.54177   standard deviation: 1.59429

# final run - state 1 sojourn time frequency distribution - sample size: 0

# absorption probability of state 2: 1

# state 2 sojourn time frequency distribution - sample size: 0

# final run - state 2 sojourn time frequency distribution - sample size: 80
# mean: 4   variance: 0   standard deviation: 0

# mixture of number of runs of state 0 per sequence distributions
# mean: 0.999821   variance: 0.000179188   standard deviation: 0.0133861

# number of runs of state 0 per sequence frequency distribution - sample size: 80
# mean: 1   variance: 0   standard deviation: 0

# mixture of number of runs of state 1 per sequence distributions
# mean: 0.99999   variance: 9.99811e-06   standard deviation: 0.00316198

# number of runs of state 1 per sequence frequency distribution - sample size: 80
# mean: 1   variance: 0   standard deviation: 0

# mixture of number of runs of state 2 per sequence distributions
# mean: 0.924371   variance: 0.0699089   standard deviation: 0.264403

# number of runs of state 2 per sequence frequency distribution - sample size: 80
# mean: 1   variance: 0   standard deviation: 0

# mixture of number of occurrences of state 0 per sequence distributions
# mean: 1.57419   variance: 0.464825   standard deviation: 0.68178

# number of occurrences of state 0 per sequence frequency distribution - sample size: 80
# mean: 1.525   variance: 0.252532   standard deviation: 0.502525

# mixture of number of occurrences of state 1 per sequence distributions
# mean: 5.1974   variance: 2.79269   standard deviation: 1.67113

# number of occurrences of state 1 per sequence frequency distribution - sample size: 80
# mean: 5.3   variance: 2.54177   standard deviation: 1.59429

# mixture of number of occurrences of state 2 per sequence distributions
# mean: 4.05341   variance: 5.93274   standard deviation: 2.43572

# number of occurrences of state 2 per sequence frequency distribution - sample size: 80
# mean: 4   variance: 0   standard deviation: 0

1 OUTPUT_PROCESS

OUTPUT_PROCESS 1 : NONPARAMETRIC

STATE 0 OBSERVATION_DISTRIBUTION
OUTPUT 0 : 0.824085
OUTPUT 1 : 0.140924
OUTPUT 2 : 0.034991

STATE 1 OBSERVATION_DISTRIBUTION
OUTPUT 0 : 0.397957
OUTPUT 1 : 0.572064
OUTPUT 2 : 0.0299782

STATE 2 OBSERVATION_DISTRIBUTION
OUTPUT 3 : 1

# observation probability matrix

#    0          1          2          3          
# 0  0.824085   0.140924   0.034991   0          
# 1  0.397957   0.572064   0.0299782  0          
# 2  0          0          0          1          

# probability of no-occurrence of output 0: 0.0105467

# time up to the first occurrence of output 0 distribution
# mean: 0.27889   variance: 0.593013   standard deviation: 0.770073

# time up to the first occurrence of output 0 frequency distribution - sample size: 78
# mean: 0.217949   variance: 0.354479   standard deviation: 0.595381

# probability of no-occurrence of output 1: 0.0239234

# time up to the first occurrence of output 1 distribution
# mean: 1.77181   variance: 1.63857   standard deviation: 1.28007

# time up to the first occurrence of output 1 frequency distribution - sample size: 76
# mean: 1.73684   variance: 1.47649   standard deviation: 1.21511

# probability of no-occurrence of output 2: 0.80729

# time up to the first occurrence of output 2 distribution
# mean: 2.85712   variance: 5.17091   standard deviation: 2.27396

# time up to the first occurrence of output 2 frequency distribution - sample size: 14
# mean: 2.42857   variance: 3.64835   standard deviation: 1.91007

# time up to the first occurrence of output 3 distribution
# mean: 6.81784   variance: 3.48697   standard deviation: 1.86734

# time up to the first occurrence of output 3 frequency distribution - sample size: 80
# mean: 6.825   variance: 2.95633   standard deviation: 1.7194

# probability of leaving output 0: 0.292278

# output 0 recurrence time distribution
# mean: 1.74036   variance: 1.22595   standard deviation: 1.10723

# output 0 recurrence time frequency distribution - sample size: 193
# mean: 1.84456   variance: 1.93405   standard deviation: 1.3907

# probability of leaving output 1: 0.302808

# output 1 recurrence time distribution
# mean: 1.48706   variance: 0.644395   standard deviation: 0.802742

# output 1 recurrence time frequency distribution - sample size: 182
# mean: 1.34615   variance: 0.382278   standard deviation: 0.618286

# probability of leaving output 2: 0.907398

# output 2 recurrence time distribution
# mean: 2.84097   variance: 3.06814   standard deviation: 1.75161

# output 2 recurrence time frequency distribution - sample size: 3
# mean: 2.66667   variance: 2.33333   standard deviation: 1.52753

# output 3 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# output 3 recurrence time frequency distribution - sample size: 240
# mean: 1   variance: 0   standard deviation: 0

# output 0 sojourn time distribution
# mean: 1.69359   variance: 0.979476   standard deviation: 0.989685
# coefficient of variation: 0.584372

# output 0 sojourn time frequency distribution - sample size: 160
# mean: 1.69375   variance: 0.993671   standard deviation: 0.996831

# final run - output 0 sojourn time frequency distribution - sample size: 0

# output 1 sojourn time distribution
# mean: 1.85049   variance: 1.37238   standard deviation: 1.17149
# coefficient of variation: 0.633069

# output 1 sojourn time frequency distribution - sample size: 127
# mean: 2.0315   variance: 2.88789   standard deviation: 1.69938

# final run - output 1 sojourn time frequency distribution - sample size: 0

# output 2 sojourn time distribution
# mean: 1.0256   variance: 0.0249454   standard deviation: 0.157941
# coefficient of variation: 0.153999

# output 2 sojourn time frequency distribution - sample size: 16
# mean: 1.0625   variance: 0.0625   standard deviation: 0.25

# final run - output 2 sojourn time frequency distribution - sample size: 0

# absorption probability of output 3: 1

# output 3 sojourn time frequency distribution - sample size: 0

# final run - output 3 sojourn time frequency distribution - sample size: 80
# mean: 4   variance: 0   standard deviation: 0

# mixture of number of runs of output 0 per sequence distributions
# mean: 1.98291   variance: 0.625389   standard deviation: 0.790815

# number of runs of output 0 per sequence frequency distribution - sample size: 80
# mean: 2   variance: 0.582278   standard deviation: 0.763072

# mixture of number of runs of output 1 per sequence distributions
# mean: 1.72944   variance: 0.609115   standard deviation: 0.780458

# number of runs of output 1 per sequence frequency distribution - sample size: 80
# mean: 1.5875   variance: 0.549209   standard deviation: 0.741086

# mixture of number of runs of output 2 per sequence distributions
# mean: 0.205367   variance: 0.191507   standard deviation: 0.437615

# number of runs of output 2 per sequence frequency distribution - sample size: 80
# mean: 0.2   variance: 0.212658   standard deviation: 0.461149

# mixture of number of runs of output 3 per sequence distributions
# mean: 0.924371   variance: 0.0699089   standard deviation: 0.264403

# number of runs of output 3 per sequence frequency distribution - sample size: 80
# mean: 1   variance: 0   standard deviation: 0

# mixture of number of occurrences of output 0 per sequence distributions
# mean: 3.36561   variance: 2.21241   standard deviation: 1.48742

# number of occurrences of output 0 per sequence frequency distribution - sample size: 80
# mean: 3.3875   variance: 1.96187   standard deviation: 1.40067

# mixture of number of occurrences of output 1 per sequence distributions
# mean: 3.19509   variance: 2.38143   standard deviation: 1.54319

# number of occurrences of output 1 per sequence frequency distribution - sample size: 80
# mean: 3.225   variance: 4.15127   standard deviation: 2.03747

# mixture of number of occurrences of output 2 per sequence distributions
# mean: 0.210891   variance: 0.207311   standard deviation: 0.455314

# number of occurrences of output 2 per sequence frequency distribution - sample size: 80
# mean: 0.2125   variance: 0.245411   standard deviation: 0.49539

# mixture of number of occurrences of output 3 per sequence distributions
# mean: 4.05341   variance: 5.93274   standard deviation: 2.43572

# number of occurrences of output 3 per sequence frequency distribution - sample size: 80
# mean: 4   variance: 0   standard deviation: 0

# distances between observation distributions for consecutive states
# _        0.43114  _        
# _        _        1        
# _        _        _        

# sequence length frequency distribution - sample size: 80
# mean: 10.825   variance: 2.95633   standard deviation: 1.7194

# cumulated length: 866

# information of the sequences in the iid case: -1012.66 (-1.16935)

# log-likelihood of the state sequences: -604.795   (normalized: -0.698377)

# state sequence entropy: 61.4354   (normalized: 0.0709416)

# log-likelihood of the observed sequences: -568.145   (normalized: -0.656057)

# 8 free parameters   2 * penalyzed log-likelihood (AIC): -1152.29

# 8 free parameters   2 * penalyzed log-likelihood (AICc): -1152.46

# 8 free parameters   2 * penalyzed log-likelihood (BIC): -1190.4

# 8 free parameters   2 * penalyzed log-likelihood (BICc): -1136.29

# 8 free parameters   2 * penalyzed log-likelihood (ICL): -1313.27

# 8 free parameters   2 * penalyzed log-likelihood (ICLc): -1259.16
