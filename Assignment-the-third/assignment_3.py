#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="'-f' to specify filename to process")
parser.add_argument("-f1", "--fn_one", help="enter filename one", required=True)
parser.add_argument("-f2", "--fn_two", help="input filename two", required=True)
parser.add_argument("-f3", "--fn_three", help="enter filename three", required=True)
parser.add_argument("-f4", "--fn_four", help="input filename four", required=True)
parser.add_argument("-ind", "--ind_list", help="input filename index list", required=True)
parser.add_argument("-q", "--qscore_cutoff", help="set cutoff for q-score", type=int, required=True)
args = parser.parse_args()

r_one = args.fn_one
r_two = args.fn_two
r_three = args.fn_three
r_four = args.fn_four
ind_list = args.ind_list
qcut = args.qscore_cutoff

#print(ind_list)


ilist = []                              #first list of indices, without their reverse complements
with open(ind_list, "r") as ind:
#with gzip.open(in_file, "rt") as f:

    for line in ind:
        a = []
        a.append(line.split()[4])           #keys
        a.append(line.split()[3])           #values

        ilist.append(a)

    ilist.pop(0)

print("ilist below")
print(ilist)

just_ind = []

for x in range(len(ilist)):
    just_ind.append(ilist[x][0])

# This list gives just the indexes, without their labeling

#ilist looks like it passes tests for indexes


def convq(c):
    p = (ord(c) - 33)
    return p


#see if index passes the q-score cutoff portion - returns boolean True/False -
# goes through and checks to make sure each positions q-score is above the cutoff

# Starts set to: True
# The following loop continues while flag is True
# Moves through length of index nt by nt, and if any nt is below cutoff, flag becomes False
# Loop ends when flag is False, else it returns True - the default value of flag

def cutoff(i):
    flag = True
    for x in range(len(i)):
            #print(convq(i[x]))
        if convq(i[x]) < qcut:
            flag = False
            return flag
                
    return flag

#test_ind = "#AAFFJJJ"

#print(cutoff(test_ind))
#print("cutoff function test - return False")

# False return test passed - both convq and cutoff fn's work

#test_ind_two = "JJJJJJJ"
#print(cutoff(test_ind_two))
#print("cutoff fn test - return True")

# True return test passed - the cutoff fn has passed both test cases - it works!!



def revc(astr):
    b = astr.replace("A",'t').replace("T", 'a').replace("C", 'g').replace("G", 'c')
    b = b.upper()
    b = b[::-1]
    
    return b

### Rev comp function works


ind_dict = {}

for x in range(len(ilist)):
    ind_dict[ilist[x][0]] = (revc(ilist[x][0]))



#print(ind_dict)
#Now index dictionary is built

#initiating file list below - list of output files

ivalues = []

for x in range(len(ilist)):
    ivalues.append(ilist[x][1])

ind_label = {}

for x in range(len(ilist)):
    ind_label[ilist[x][0]] = ilist[x][1]

#print(ind_label)

#dictionary with list of indexes and labels has been built

hop_for = open("index_hopped_forward.fq", "w")
hop_rev = open("index_hopped_reverse.fq", "w")
unk_for = open("unknown_lowq_forward.fq", "w")
unk_rev = open("unknown_lowq_reverse.fq", "w")
stats = open("statistics.txt", "w")



import gzip

onelist = []
twolist = []
threelist = []
fourlist = []
#with open(in_file, "r") as f:
with gzip.open(r_one, "rt") as f_one, gzip.open(r_two, "rt") as f_two, gzip.open(r_three, "rt") as f_three, gzip.open(r_four, "rt") as f_four:
#with open(r_one, "rt") as f_one, open(r_two, "rt") as f_two, open(r_three, "rt") as f_three, open(r_four, "rt") as f_four:
    lc = 0
    rec = 0
    match_count = 0
    hop_count = 0
    unk_count = 0
    total_read = {}
    # Dictionary for keeping track of amount of reads per matched index
    for line in zip(f_one, f_two, f_three, f_four):
        lc += 1
        one = line[0].strip()
        two = line[1].strip()
        three = line[2].strip()
        four = line[3].strip()
        if lc // 4 == rec:
            onelist.append(one)
            twolist.append(two)
            threelist.append(three)
            fourlist.append(four)
        else:
            onelist.append(one)
            twolist.append(two)
            threelist.append(three)
            fourlist.append(four)
            rec += 1

            #print("onelist")
            #print(twolist)

            # Test passed ^ holds records correctly
            # Tested for each of the four lists: one, two, three and fourlist
            # All passed
            # Records get erased after looping through

            #print(twolist[1])
            #print(threelist[1])
            
            onelist[0] = onelist[0] + " " + twolist[1] + "-" + (threelist[1])       # Changed from revc(3list[1])
            fourlist[0] = fourlist[0] + " " + twolist[1] + "-" + (threelist[1])     # Changed from revc(3list[1])

            if cutoff(twolist[3]) and cutoff(threelist[3]):
                #body of main
                if (twolist[1] in just_ind) and ( (revc(threelist[1])) in just_ind):
                    if twolist[1] == (revc(threelist[1])):
                        #sort to matched list set
                        name = ind_label[twolist[1]]
                        # Name gives the name of the index based on the index sequence, i.e.:
                        # ind_label["ATTAGCCG"] >> "A2"
                        match_for = open("%s_match_forward.fq" % name, "a")
                        match_rev = open("%s_match_reverse.fq" % name, "a")
                        # Find header - add to dictionary of matches
                        for f in onelist:
                            match_for.write(f + '\n')
                        for g in fourlist:
                            match_rev.write(g + '\n')
                        
                        match_count += 1
                        if name in total_read:
                            total_read[name] += 1
                        if name not in total_read:
                            total_read[name] = 1
                        
                        # Added ^ to keep track of percentages of certain reads

                    else:
                        #sort to hopped
                        for f in onelist:
                            hop_for.write(f + '\n')
                        for g in fourlist:
                            hop_rev.write(g + '\n')
                        hop_count += 1


                else:
                    #sort to unknown/low quality
                    for f in onelist:
                        unk_for.write(f + '\n')
                    for g in fourlist:
                        unk_rev.write(g + '\n')
                    unk_count += 1
            
            else:
                #sort to unknown/low quality
                for f in onelist:
                    unk_for.write(f + '\n')
                for g in fourlist:
                    unk_rev.write(g + '\n')
                unk_count += 1


            


            
            #clear running lists below here and start over
            onelist = []
            twolist = []
            threelist = []
            fourlist = []


overall = match_count + hop_count + unk_count

# total_read is the dictionary with the number of occurences of each index
# Use this below to calculate the percentage of each reads occurence


for k,v in total_read.items():
    stats.write(str(k) + ":\t" + str(v/overall))

## Write to the stats page below here
#stats.write(hop_count)





