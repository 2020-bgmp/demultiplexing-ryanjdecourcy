#!/usr/bin/env python

onelist = ['@K00337:83:HJKJNBBXX:8:1101:2219:1191 1:N:0:1 NACCGGAT-TACCGGAN', 'CNAGGACCTCACCCCAAATCTCCCTGGAGCTGGCCTTCTTGGAAACGCTCCCTGCTGAGGCTGGGGGCAGGTGCTAGTCAGTACCACAGCAATACCTTCGG', '+', 'A#AFFFJJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJFJFJJJJJJJJJJJJJFJJJJJJJJJJJJ']
twolist = ['@K00337:83:HJKJNBBXX:8:1101:2219:1191 2:N:0:1', 'GTAGCGTA', '+', 'JJJJJJJJ']
threelist = ['@K00337:83:HJKJNBBXX:8:1101:2219:1191 3:N:0:1', 'TACGCTAC', '+', 'JJJJJJJJ']
fourlist = ['@K00337:83:HJKJNBBXX:8:1101:2219:1191 4:N:0:1 NACCGGAT-TACCGGAN', 'NATGTCATGGTGCTAAGGGTTTCCTGGTGCCGAAGGTATTGCTGTGGTACTGACTAGCACCTGCCCCCAGCCTCAGCAGGGAGCGTTTCCAAGAAGGCCAG', '+', '#AAFFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJAJFJJJJJJJJJJJJJ']
ilist = [['GTAGCGTA', 'B1'], ['CGATCGAT', 'A5'], ['GATCAAGG', 'C1'], ['AACAGCGA', 'B9'], ['TAGCCATG', 'C9'], ['CGGTAATC', 'C3'], ['CTCTGGAT', 'B3'], ['TACCGGAT', 'C4'], ['CTAGCTCA', 'A11'], ['CACTTCAC', 'C7'], ['GCTACTCT', 'B2'], ['ACGATCAG', 'A1'], ['TATGGCAC', 'B7'], ['TGTTCCGT', 'A3'], ['GTCCTAAG', 'B4'], ['TCGACAAG', 'A12'], ['TCTTCGAC', 'C10'], ['ATCATGCG', 'A2'], ['ATCGTGGT', 'C2'], ['TCGAGAGT', 'A10'], ['TCGGATTC', 'B8'], ['GATCTTGC', 'A7'], ['AGAGTCCA', 'B10'], ['AGGATAGC', 'A8']]

def revc(astr):
    b = astr.replace("A",'t').replace("T", 'a').replace("C", 'g').replace("G", 'c')
    b = b.upper()
    b = b[::-1]
    
    return b

def cutoff(i):
    flag = True
    for x in range(len(i)):
            #print(convq(i[x]))
        if convq(i[x]) < qcut:
            flag = False
            return flag
                
    return flag

############ Gives list with just indexes and not their names
just_ind = []

for x in range(len(ilist)):
    just_ind.append(ilist[x][0])
# End - just_ind list


#############################
ind_label = {}

for x in range(len(ilist)):
    ind_label[ilist[x][0]] = ilist[x][1]
# Ind label dictonary is added
################################

def convq(c):
    p = (ord(c) - 33)
    return p
# Added convq function ^^
qcut = 33

total_read = {}

match_count = 0



# The line below needs to be cutoff(twolist[3]) instead of twolist[1]
if cutoff(twolist[3]) and cutoff(threelist[3]):
                #body of main
                if (twolist[1] in just_ind) and ( (revc(threelist[1])) in just_ind):
                    if twolist[1] == (revc(threelist[1])):
                        #sort to matched list set
                        name = ind_label[twolist[1]]
                        match_for = open("%s_match_forward.fq" % name, "w")
                        match_rev = open("%s_match_reverse.fq" % name, "w")
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
                        
                        # Added ^ to keep track of percentages of certain reads'''

#print(revc("GTAGCGTA"))
# Used to make reverse complement, so that matched portion of the program can be tested

print(match_count)