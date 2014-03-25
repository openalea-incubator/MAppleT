HIDDEN_SEMI-MARKOV_CHAIN

3 STATES

INITIAL_PROBABILITIES
0.921135   0.0788652  0          

TRANSITION_PROBABILITIES
0          1          0          
0          0          1          
0          0          1          

# transient class: state 0
# transient class: state 1
# recurrent class: state 2 (absorbing state)

# probability of no-occurrence of state 0: 0.0788652

# time up to the first occurrence of state 0 distribution
# mean: 0   variance: 0   standard deviation: 0

# time up to the first occurrence of state 0 frequency distribution - sample size: 19
# mean: 0   variance: 0   standard deviation: 0

# time up to the first occurrence of state 1 distribution
# mean: 1.32663   variance: 0.466929   standard deviation: 0.683322

# time up to the first occurrence of state 1 frequency distribution - sample size: 20
# mean: 1.5   variance: 0.368421   standard deviation: 0.606977

# time up to the first occurrence of state 2 distribution
# mean: 6.78873   variance: 3.64392   standard deviation: 1.90891

# time up to the first occurrence of state 2 frequency distribution - sample size: 20
# mean: 6.8   variance: 3.64211   standard deviation: 1.90843

# probability of leaving state 0: 0.69434

# state 0 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 0 recurrence time frequency distribution - sample size: 11
# mean: 1   variance: 0   standard deviation: 0

# probability of leaving state 1: 0.182994

# state 1 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 1 recurrence time frequency distribution - sample size: 86
# mean: 1   variance: 0   standard deviation: 0

# state 2 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# state 2 recurrence time frequency distribution - sample size: 204
# mean: 1   variance: 0   standard deviation: 0

STATE 0 OCCUPANCY_DISTRIBUTION
BINOMIAL   INF_BOUND : 1   SUP_BOUND : 3   PROBABILITY : 0.220109
# mean: 1.44022   variance: 0.343322   standard deviation: 0.585937
# coefficient of skewness: 0.955364   coefficient of kurtosis: -0.0872801
# coefficient of variation: 0.406839

# state 0 sojourn time frequency distribution - sample size: 19
# mean: 1.57895   variance: 0.25731   standard deviation: 0.507257

# final run - state 0 sojourn time frequency distribution - sample size: 0

STATE 1 OCCUPANCY_DISTRIBUTION
BINOMIAL   INF_BOUND : 2   SUP_BOUND : 47   PROBABILITY : 0.0769928
# mean: 5.46467   variance: 3.19792   standard deviation: 1.78827
# coefficient of skewness: 0.47309   coefficient of kurtosis: 0.17937
# coefficient of variation: 0.327242

# state 1 sojourn time frequency distribution - sample size: 20
# mean: 5.3   variance: 3.06316   standard deviation: 1.75019

# final run - state 1 sojourn time frequency distribution - sample size: 0

# absorption probability of state 2: 1

# state 2 sojourn time frequency distribution - sample size: 0

# final run - state 2 sojourn time frequency distribution - sample size: 20
# mean: 11.2   variance: 3.64211   standard deviation: 1.90843

# number of runs of state 0 per length 18 sequence distribution
# mean: 0.921135   variance: 0.0726455   standard deviation: 0.269528
# coefficient of skewness: -3.12498   coefficient of kurtosis: 7.76548

# number of runs of state 0 per sequence frequency distribution - sample size: 20
# mean: 0.95   variance: 0.05   standard deviation: 0.223607
# coefficient of skewness: -4.47214   coefficient of kurtosis: 14.15

# number of runs of state 1 per length 18 sequence distribution
# mean: 1   variance: 0   standard deviation: 0

# number of runs of state 1 per sequence frequency distribution - sample size: 20
# mean: 1   variance: 0   standard deviation: 0

# number of runs of state 2 per length 18 sequence distribution
# mean: 0.999997   variance: 2.81163e-06   standard deviation: 0.00167679
# coefficient of skewness: -596.374   coefficient of kurtosis: 355660

# number of runs of state 2 per sequence frequency distribution - sample size: 20
# mean: 1   variance: 0   standard deviation: 0

# number of occurrences of state 0 per length 18 sequence distribution
# mean: 1.32663   variance: 0.466929   standard deviation: 0.683322
# coefficient of skewness: 0.319695   coefficient of kurtosis: 0.0528491

# number of occurrences of state 0 per sequence frequency distribution - sample size: 20
# mean: 1.5   variance: 0.368421   standard deviation: 0.606977
# coefficient of skewness: -0.784528   coefficient of kurtosis: -0.576531

# number of occurrences of state 1 per length 18 sequence distribution
# mean: 5.46467   variance: 3.19791   standard deviation: 1.78827
# coefficient of skewness: 0.473058   coefficient of kurtosis: 0.179094

# number of occurrences of state 1 per sequence frequency distribution - sample size: 20
# mean: 5.3   variance: 3.06316   standard deviation: 1.75019
# coefficient of skewness: 1.71345   coefficient of kurtosis: 3.37167

# number of occurrences of state 2 per length 18 sequence distribution
# mean: 11.2087   variance: 3.66483   standard deviation: 1.91438
# coefficient of skewness: -0.400129   coefficient of kurtosis: 0.137167

# number of occurrences of state 2 per sequence frequency distribution - sample size: 20
# mean: 11.2   variance: 3.64211   standard deviation: 1.90843
# coefficient of skewness: -1.57904   coefficient of kurtosis: 3.47336

1 OUTPUT_PROCESS

OUTPUT_PROCESS 1 : NONPARAMETRIC

STATE 0 OBSERVATION_DISTRIBUTION
OUTPUT 0 : 0.963255
OUTPUT 1 : 9.98398e-05
OUTPUT 2 : 0.0366449

STATE 1 OBSERVATION_DISTRIBUTION
OUTPUT 0 : 0.396922
OUTPUT 1 : 0.584552
OUTPUT 2 : 0.0185257

STATE 2 OBSERVATION_DISTRIBUTION
OUTPUT 3 : 1

# observation probability matrix

#    0            1            2            3            
# 0  0.963255     9.98398e-05  0.0366449    0            
# 1  0.396922     0.584552     0.0185257    0            
# 2  0            0            0            1            

# probability of no-occurrence of output 0: 0.00898801

# time up to the first occurrence of output 0 distribution
# mean: 0.132112   variance: 0.316015   standard deviation: 0.562152

# time up to the first occurrence of output 0 frequency distribution - sample size: 20
# mean: 0.25   variance: 0.828947   standard deviation: 0.910465

# probability of no-occurrence of output 1: 0.0217269

# time up to the first occurrence of output 1 distribution
# mean: 1.95521   variance: 1.34703   standard deviation: 1.16062

# time up to the first occurrence of output 1 frequency distribution - sample size: 19
# mean: 1.84211   variance: 0.918129   standard deviation: 0.95819

# probability of no-occurrence of output 2: 0.859991

# time up to the first occurrence of output 2 distribution
# mean: 2.53788   variance: 5.34035   standard deviation: 2.31092

# time up to the first occurrence of output 2 frequency distribution - sample size: 3
# mean: 2   variance: 3   standard deviation: 1.73205

# time up to the first occurrence of output 3 distribution
# mean: 6.78873   variance: 3.64392   standard deviation: 1.90891

# time up to the first occurrence of output 3 frequency distribution - sample size: 20
# mean: 6.8   variance: 3.64211   standard deviation: 1.90843

# probability of leaving output 0: 0.287505

# output 0 recurrence time distribution
# mean: 1.7432   variance: 1.25031   standard deviation: 1.11817

# output 0 recurrence time frequency distribution - sample size: 49
# mean: 1.83673   variance: 2.51446   standard deviation: 1.5857

# probability of leaving output 1: 0.306235

# output 1 recurrence time distribution
# mean: 1.42606   variance: 0.536734   standard deviation: 0.732621

# output 1 recurrence time frequency distribution - sample size: 45
# mean: 1.24444   variance: 0.279798   standard deviation: 0.528959

# probability of leaving output 2: 0.934319

# output 2 recurrence time distribution
# mean: 2.952   variance: 3.33456   standard deviation: 1.82608

# output 2 recurrence time frequency distribution - sample size: 0

# output 3 recurrence time distribution
# mean: 1   variance: 0   standard deviation: 0

# output 3 recurrence time frequency distribution - sample size: 204
# mean: 1   variance: 0   standard deviation: 0

# output 0 sojourn time distribution
# mean: 1.70707   variance: 0.979107   standard deviation: 0.989498
# coefficient of variation: 0.579647

# output 0 sojourn time frequency distribution - sample size: 39
# mean: 1.76923   variance: 1.18219   standard deviation: 1.08728

# final run - output 0 sojourn time frequency distribution - sample size: 0

# output 1 sojourn time distribution
# mean: 1.91361   variance: 1.44727   standard deviation: 1.20302
# coefficient of variation: 0.628668

# output 1 sojourn time frequency distribution - sample size: 28
# mean: 2.28571   variance: 3.98942   standard deviation: 1.99735

# final run - output 1 sojourn time frequency distribution - sample size: 0

# output 2 sojourn time distribution
# mean: 1.01776   variance: 0.0174491   standard deviation: 0.132095
# coefficient of variation: 0.129789

# output 2 sojourn time frequency distribution - sample size: 3
# mean: 1   variance: 0   standard deviation: 0

# final run - output 2 sojourn time frequency distribution - sample size: 0

# absorption probability of output 3: 1

# output 3 sojourn time frequency distribution - sample size: 0

# final run - output 3 sojourn time frequency distribution - sample size: 20
# mean: 11.2   variance: 3.64211   standard deviation: 1.90843

# number of runs of output 0 per length 18 sequence distribution
# mean: 2.01511   variance: 0.641648   standard deviation: 0.801029
# coefficient of skewness: 0.343153   coefficient of kurtosis: 0.1278

# number of runs of output 0 per sequence frequency distribution - sample size: 20
# mean: 1.95   variance: 0.576316   standard deviation: 0.759155
# coefficient of skewness: 0.086213   coefficient of kurtosis: -1.26252

# number of runs of output 1 per length 18 sequence distribution
# mean: 1.66888   variance: 0.559864   standard deviation: 0.748241
# coefficient of skewness: 0.504508   coefficient of kurtosis: 0.207705

# number of runs of output 1 per sequence frequency distribution - sample size: 20
# mean: 1.4   variance: 0.357895   standard deviation: 0.598243
# coefficient of skewness: -0.393309   coefficient of kurtosis: -0.837024

# number of runs of output 2 per length 18 sequence distribution
# mean: 0.147149   variance: 0.14008   standard deviation: 0.374273
# coefficient of skewness: 2.41847   coefficient of kurtosis: 5.22982

# number of runs of output 2 per sequence frequency distribution - sample size: 20
# mean: 0.15   variance: 0.134211   standard deviation: 0.366348
# coefficient of skewness: 2.12306   coefficient of kurtosis: 1.60098

# number of runs of output 3 per length 18 sequence distribution
# mean: 0.999997   variance: 2.81163e-06   standard deviation: 0.00167679
# coefficient of skewness: -596.374   coefficient of kurtosis: 355660

# number of runs of output 3 per sequence frequency distribution - sample size: 20
# mean: 1   variance: 0   standard deviation: 0

# number of occurrences of output 0 per length 18 sequence distribution
# mean: 3.44694   variance: 2.29213   standard deviation: 1.51398
# coefficient of skewness: 0.416627   coefficient of kurtosis: 0.170716

# number of occurrences of output 0 per sequence frequency distribution - sample size: 20
# mean: 3.45   variance: 2.05   standard deviation: 1.43178
# coefficient of skewness: 0.290788   coefficient of kurtosis: -0.988858

# number of occurrences of output 1 per length 18 sequence distribution
# mean: 3.19452   variance: 2.41996   standard deviation: 1.55562
# coefficient of skewness: 0.445734   coefficient of kurtosis: 0.207136

# number of occurrences of output 1 per sequence frequency distribution - sample size: 20
# mean: 3.2   variance: 4.37895   standard deviation: 2.09259
# coefficient of skewness: 1.1227   coefficient of kurtosis: 0.972416

# number of occurrences of output 2 per length 18 sequence distribution
# mean: 0.149851   variance: 0.147919   standard deviation: 0.384602
# coefficient of skewness: 2.53378   coefficient of kurtosis: 6.25552

# number of occurrences of output 2 per sequence frequency distribution - sample size: 20
# mean: 0.15   variance: 0.134211   standard deviation: 0.366348
# coefficient of skewness: 2.12306   coefficient of kurtosis: 1.60098

# number of occurrences of output 3 per length 18 sequence distribution
# mean: 11.2087   variance: 3.66483   standard deviation: 1.91438
# coefficient of skewness: -0.400129   coefficient of kurtosis: 0.137167

# number of occurrences of output 3 per sequence frequency distribution - sample size: 20
# mean: 11.2   variance: 3.64211   standard deviation: 1.90843
# coefficient of skewness: -1.57904   coefficient of kurtosis: 3.47336

# distances between observation distributions for consecutive states
# _         0.584453  _         
# _         _         1         
# _         _         _         

# sequence length frequency distribution - sample size: 20
# mean: 18   variance: 0   standard deviation: 0

# cumulated length: 360

# information of the sequences in the iid case: -345.171 (-0.958808)

# log-likelihood of the state sequences: -141.233   (normalized: -0.392314)

# state sequence entropy: 11.7434   (normalized: 0.0326206)

# log-likelihood of the observed sequences: -133.974   (normalized: -0.37215)

# 9 free parameters   2 * penalyzed log-likelihood (AIC): -285.948

# 9 free parameters   2 * penalyzed log-likelihood (AICc): -286.462

# 9 free parameters   2 * penalyzed log-likelihood (BIC): -320.923

# 9 free parameters   2 * penalyzed log-likelihood (BICc): -267.948

# 9 free parameters   2 * penalyzed log-likelihood (ICL): -344.41

# 9 free parameters   2 * penalyzed log-likelihood (ICLc): -291.435
