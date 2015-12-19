#! /bin/env python

###############################
# a.succurro ATgmail.com # 2011 #
###############################

# python script to reorder event lists
# in the format (from event challenge)
# RunNumber  EventNumber

import math as math
import sys as sys

import os
import fileinput
from sys import stdout
import fileinput


if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please, provide the root file name"
    sys.exit(1)

#declare global stuff here
try:
	fout = open(filename+"_ordered.txt", 'wa')
except IOError:
	print "cannot open file" , filename
				
#__________main function_________________

if __name__=="__main__":

        listevt = []

        for line in fileinput.input(filename+".txt"):
                newline = line.rstrip().lstrip()
                splitted = newline.split(' ')
                run = int(splitted[0])
                event = int(splitted[1])
                prov = [run, event]
                listevt.append(prov)

        listevt.sort()

        for evt in listevt:
                
                fout.write("%s %s\n" % (evt[0], evt[1]))

        fout.close()
