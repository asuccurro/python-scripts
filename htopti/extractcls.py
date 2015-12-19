#! /bin/env python
#==================== ^_^ ====================#
# succurro ATifae.es
# fill py files with yield dictionaries
#==================== ^_^ ====================#
import os, sys
from sys import stdout
import fileinput
import commands
#import argparse
import optparse
import math as math
from array import array

#==================== ^_^ ====================#
def options():
        '''define here in-line arguments'''
        #parser = argparse.ArgumentParser(description='I do nice things with the right inputs!')
        #parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        parser = optparse.OptionParser(description='I do nice things with the right inputs!')
        parser.add_option("-v", "--verbose", dest='verbose', help="increase output verbosity", action="store_true")
	parser.add_option("-i", "--inputfile", dest='inputfile', help="input file obtained like  grep gclsexpbmed */*/*out > clsvals.txt", default="clsvals.txt")
        opts, args = parser.parse_args()
        if opts.verbose:
                print "verbosity turned on"
                print opts
                print args
	return opts, args

#==================== ^_^ ====================#
def main():
	'''send ftm jobs'''
	opts, args = options()
	
        outpath = "./"
	try:
		outFile = open(outpath+'CLSvalues.py', 'w') 
	except IOError:
		print "cannot open out file"

	#try:
	#	inFile = open(opts.inputfile,'r')
	#except IOError:
	#	print "cannot open in file"

	dictOfCuts = {}

	for l in fileinput.input(opts.inputfile):
		splitpath = l.split("/")
		if opts.verbose:
			print "size of line split at '/': ",len(splitpath)
		htcut = splitpath[0][-3:]
		htcutstring = "H_T > "+htcut+" GeV"
		vltmass = int(splitpath[1][0:3])
		clsval = float(splitpath[2].split(':')[2][1:])
		#vltmass = splitpath[1][0:3]
		#clsval = splitpath[2].split(':')[2][1:].rstrip()
		#dictOfCuts[htcut] = dictOfCuts.get(htcut, []).append( (htcutstring, vltmass, clsval) )
		if dictOfCuts.get(htcut) == None:
			dictOfCuts[htcut] = []
		else:
			dictOfCuts[htcut].append( (vltmass, clsval) )
		#dictOfCuts[htcut] = dictOfCuts.get(htcut, []).append( (vltmass, clsval) )

	#mapping mass to value for each cut
	#htcutlist = []
	#for k in dictOfCuts.keys():
	#	htcutlist.append(k)
	#	outFile.write("cut_%s = { \n" % k)
	#	for t in dictOfCuts[k]:
	#		outFile.write("\t'%s' : %s,\n" % (t[0], t[1]))
	#	outFile.write("   }\n")
	#outFile.write("htcuts = "+str(htcutlist)+"\n")

	#mapping cut to lists of masses and values, more efficient!

	outFile.write("from array import array\n\nHTcutDict = { \n")
	for k in dictOfCuts.keys():
		outFile.write("\t'%s' :\t [ \n\t\t array( 'd', %s ), \n\t\t array( 'd', %s) \n\t\t],\n" % (k, str(list(zip(*dictOfCuts[k])[0])), str(list(zip(*dictOfCuts[k])[1])) ))
	outFile.write("   }\n")
	outFile.close()
 #	    print " & %d  & %.1f \t$\pm$ \t%.1f \t" % (hist.GetEntries(),hist.IntegralAndError(1,-1, err), err)
	    #print "  & %.1f \t$\pm$ \t%.1f \t" % (hist.IntegralAndError(1,-1, err), err)



#==================== ^_^ ====================#
if __name__=="__main__":
	main()
