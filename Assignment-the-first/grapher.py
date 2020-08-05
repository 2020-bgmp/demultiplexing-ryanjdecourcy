#!/usr/bin/env python
#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description=" '-f' to specify filename")
parser.add_argument("-f", "--filename", help="enter output filename", required=True)
#parser.add_argument("-r", "--read", help="input Read number, ex.: R1", required=True)
#parser.add_argument("-l", "--read_length", help="input the read length", required=True)
args = parser.parse_args()

in_file = args.filename
#read = args.read
#read_len = int(args.read_length)

#alist = []

with open(in_file, "r") as f:
    for line in f:
        alist = (line.split())
    
    
blist = []

blist.append(float(alist[0][2:]))

for x in range(1, len(alist)):
    blist.append(float(alist[x]))


#############################
# GRAPHING PORTION STARTS HERE #

out_graph = "R4_dist.png"


import matplotlib.pyplot as plt

plt.figure(figsize=(10,10))

plt.xlabel("Nucleotide Position")
plt.ylabel("Mean Value Q-Score")
plt.bar(list(x for x in range(1, (len(blist) + 1))), blist)
plt.show()
plt.savefig("R4distribution.png")
