import cPickle
import csv as pycsv

plan_file = "plan1.csv"
sequence_file = "sequences.seq"
merged_file = "pleqplan.csv"

##########################################################
###This part is to re-organise the sequence file with 9###
##########################################################
#The original sequence file produced by Evelyne
ori_seq_file = sequence_file

#seq is the list of original sequences
op = open(ori_seq_file)
seq = cPickle.load(op)
op.close()

sequence_lengths = []
for i in seq:
    sequence_lengths.append(len(i))
#upper length for all sequences
length_upper = max(sequence_lengths)
print length_upper
for i in seq:
    if len(i) < length_upper:
        i += [9]*(length_upper-len(i))
    print len(i)
    print i
    print "\n"

op = open(sequence_file, "w")
cPickle.dump(seq, op, 0)
op.close()

#####################################################
###The following part is to make the pleaplan file###
#####################################################

gt = open(sequence_file)
sequences_list = cPickle.load(gt)
seq_nbr = len(sequences_list)

op = open(merged_file, "w")

plan_read = pycsv.reader(open(plan_file, "rb"), delimiter=",")

#Id of the combinations
cid = 0
for row in plan_read:
    if row[0] != "":
        for i in range(seq_nbr):
            new_row = ""
            for e in row:
                new_row += e
                new_row +=","
            new_row += str(i) + "," + str(cid) + "\n"
            op.write(new_row)
            cid += 1
    else:
        new_row = ""
        for e in row:
            new_row += e
            new_row +=","
        new_row += "sequence" + "," + "combination" + "\n"
        op.write(new_row)

op.close()
