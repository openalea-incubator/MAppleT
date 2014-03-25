from openalea.aml import *


#Analyses of sequences for APMed project
#Sequences were generated using a specific protocol where the codes were:
# 0 Latent
# 1 Short
# 2 Long
# 3 Floral w/ short bourse shoot
# 4 Floral w/ long bourse shoot
# 5 Floral w/o bourse shoot
# 6 Sylleptic


#########################################
#                 LLEIDA                #
#########################################
seq = Sequences("seq_Lleida.csv")


Plot(seq, "Intensity")
Display(seq, Format="Line", ViewPoint="Data")
 
#Read the Markov model initialisation file
h3=HiddenSemiMarkov("Model_3_init_Lleida.hsc")
#HSMC Estimation
model3=Estimate(seq, "HIDDEN_SEMI-MARKOV", h3)
#Visualization and saving the estimated model
Display(ExtractData(model3), ViewPoint="Data", Format="Line")
model3_data = Save(ExtractData(model3), "Model_3_Lleida.hsc")

#More visualization
Plot(model3, "FirstOccurrence")
Plot(model3, "Sojourn")
Plot(model3, "Intensity")
Plot(model3, "Intensity",1)
#Counting runs (nb of successive similar output) of state and observations
Plot(model3, "Counting")
Plot(model3, "Counting", 1)

#Alternative model removing the only 5 present
seq1 = Transcode(seq, [0,1,2,3,4,4,5])
h3b=HiddenSemiMarkov("Model_3b_init_Lleida.hsc")
model3b=Estimate(seq1, "HIDDEN_SEMI-MARKOV", h3b)
model3_data = Save(ExtractData(model3b), "Model_3b_Lleida.hsc")


#########################################
#                 CEHM                  #
#########################################

#======== MEDIUM ===============

seq = Sequences("seq_CEHM_medium.csv")

#Changing the one long into short as well as the two syleptics 
#All florals are put together with the code 2
seqall = Transcode(seq, [0,1,1,2,2,2,1])
Plot(seqall, "Intensity", 1)

seqc1 = SelectIndividual(seqall, range(1,21))
seqc2 = SelectIndividual(seqall, range(21,41))
seqc3 = SelectIndividual(seqall, range(41,61))
seqc4 = SelectIndividual(seqall, range(61,81))

Plot(seqc1, "Intensity", 1)
Plot(seqc2, "Intensity", 1)
Plot(seqc3, "Intensity", 1)
Plot(seqc4, "Intensity", 1)

seqall = AddAbsorbingRun(seqall, RunLength=4)

#Matching with a 3-states model
hall3=HiddenSemiMarkov("Model_3_init_CEHM_medium.hsc")
modelall3=Estimate(seqall, "HIDDEN_SEMI-MARKOV", hall3)
modelall3_data = Save(ExtractData(modelall3), "Model_3_CEHM_medium.hsc")

#Matching with a 2-states model
hall2=HiddenSemiMarkov("Model_2_init_CEHM_medium.hsc")
modelall2=Estimate(seqall, "HIDDEN_SEMI-MARKOV", hall2)
modelall2_data = Save(ExtractData(modelall2), "Model_2_CEHM_medium.hsc")

#======== SHORT w/ flowers ===============

seq = Sequences("seq_CEHM_short_fl.csv")

#Changing the one sylleptic to short and shifting floral w/ short from 3 to 2 and floral w/o bourse shoot from 5 to 3
seqall = Transcode(seq, [0,1,1,2,2,3,1])
Plot(seqall, "Intensity")

seqc1 = SelectIndividual(seqall, range(1,21))
seqc2 = SelectIndividual(seqall, range(21,41))
seqc3 = SelectIndividual(seqall, range(41,61))
seqc4 = SelectIndividual(seqall, range(61,81))

Plot(seqc1, "Intensity", 1)
Plot(seqc2, "Intensity", 1)
Plot(seqc3, "Intensity", 1)
Plot(seqc4, "Intensity", 1)

seqall = AddAbsorbingRun(seqall, RunLength=4)

h2=HiddenSemiMarkov("Model_2_init_CEHM_c1m.hsc")
model2=Estimate(seq_sfc1, "HIDDEN_SEMI-MARKOV", h2)
model2_data = Save(ExtractData(model2), "Model_2_CEHM_sfc1.hsc")
#h3=HiddenSemiMarkov("Model_3_init_CEHM_sfc1.hsc")
#model3=Estimate(seq_sfc1, "HIDDEN_SEMI-MARKOV", h3)
#model3_data = Save(ExtractData(model2), "Model_3_CEHM_sfc1.hsc")

Plot(model3, "Intensity",1)

#Short w/o flowers
seq = Sequences("seq_CEHM_short_nofl_C1.csv")
Plot(seq, "Intensity")

seq_snofc1 = AddAbsorbingRun(seq)

h3=HiddenSemiMarkov("Model_3_init_CEHM_sfc1.hsc")
model3=Estimate(seq_snofc1, "HIDDEN_SEMI-MARKOV", h3)
model3_data = Save(ExtractData(model3), "Model_3_CEHM_snofc1.hsc")

Plot(model3, "Intensity",1)

