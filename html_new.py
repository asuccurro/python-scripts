#!/usr/bin/env python

###############################
# a.succurro@gmail.com # 2013 #
###############################

# python script to produce .html files
# showing plots of interest
# in an ordered format

import os, sys
from sys import stdout
import fileinput
import commands
#import argparse                                                                                                                                                           
import optparse


#==================== ^_^ ====================#                                                                                                                            
def options():
        '''define here in-line arguments'''
        parser = optparse.OptionParser(description='I do nice things with the right inputs!')
        parser.add_option("-v", "--verbose", dest='verbose', help="increase output verbosity", action="store_true")
	parser.add_option('-V', '--Variables', dest='Variables', help='list of variables to plot', default='Njets25')
	parser.add_option('-C', '--Channels', dest='Channels', help='list of channels to plot', default='')
	parser.add_option('-L', '--Lep', dest='Lep', help='list of lep to plot', default='ELEMUON')
	parser.add_option('-m', '--mode', dest='mode', help='can be CHANNEL VARIABLE', default='CHANNEL')
        parser.add_option("-d", "--inputdir", dest='inputdir', help="input dir for the files", default="mydir")
	parser.add_option('-n', '--name', dest='name', help='html file name', default='index_1.html')
        opts, args = parser.parse_args()
	if opts.verbose:
                print "verbosity turned on"
                print opts
                print args
	return opts, args

def getDir(mydir, lep, ch):
	if "jet" in ch:
		#_4jetex0btagin
		d1 = ch[1:7]
		d2 = ch[7:14]
		return "%s/%s/%s/%s"%(mydir,lep,d1,d2)
	else:
		return mydir

def main():

	opts, args = options()

	variables = opts.Variables.split(' ')
	channels = opts.Channels.split(' ')
	lep = opts.Lep.split(' ')

	files = {}
	htmlindex = open('%s_%s_index.html'%(opts.mode, opts.inputdir), 'wa')
	htmlindex.write('<h2> Go to: </h2>\n <ul>\n')
	for l in lep:
		htmlindex.write('<li>%s</li>\n <ul>'%l)
		if opts.mode == 'CHANNEL':
			for c in channels:
				mydir = getDir(opts.inputdir, l, c)
				fn = l+c
				htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%(fn+'.html', c.replace('_',' ')))
				files[fn] = open(fn+'.html', 'wa')
				files[fn].write("<h1>%s</h1> \n <p> \n" % (fn+" lin scale"))
				files[fn].write("<h2> <a href=%s> go to log scale </a> </h2> \n <p> \n" % (fn+'_log.html'))
				files[fn+'_log'] = open(fn+'_log.html', 'wa')
				files[fn+'_log'].write("<h1>%s</h1> \n <p> \n" % (fn+" log scale"))
				files[fn+'_log'].write("<h2> <a href=%s> go to lin scale </a> </h2> \n <p> \n" % (fn+'.html'))
				files[fn].write("<table border=\"1\"> \n")
				files[fn+'_log'].write("<table border=\"1\"> \n")
				for v in variables:
					fullpath = "%s/%s_%s_NOMINAL.png" % (mydir, v, fn)
					fullpathlog = "%s/%s_%s_NOMINAL_logscale.png" % (mydir, v, fn)
					files[fn].write("<tr> <td> %s </td>\n" % v)
					files[fn].write("<tr> <td> <img src=\"%s\" alt=\"%s\"</img>  </td>\n" % (fullpath, fullpath))
					files[fn+'_log'].write("<tr><td> %s </td>\n" % v)
					files[fn+'_log'].write("<tr><td><img src=\"%s\" alt=\"%s\"</img></td>\n"%(fullpathlog, fullpathlog))
				files[fn].write("\n </table> \n")
				files[fn+'_log'].write("\n </table> \n")
				files[fn].close()
				files[fn+'_log'].close()

		elif opts.mode == 'ALL':
			fn = l
			htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%(fn+'.html', fn))
			files[fn] = open(fn+'.html', 'wa')
			files[fn].write("<h1>%s</h1> \n <p> \n" % (fn+" lin scale"))
			files[fn].write("<h2> <a href=%s> go to log scale </a> </h2> \n <p> \n" % (fn+'_log.html'))
			files[fn+'_log'] = open(fn+'_log.html', 'wa')
			files[fn+'_log'].write("<h1>%s</h1> \n <p> \n" % (fn+" log scale"))
			files[fn+'_log'].write("<h2> <a href=%s> go to lin scale </a> </h2> \n <p> \n" % (fn+'.html'))
			files[fn].write("<table border=\"1\">\n <tr>\n")
			files[fn+'_log'].write("<table border=\"1\">\n <tr>\n")
			for c in channels:
				files[fn].write("<td> %s </td>" % c)
				files[fn+'_log'].write("<td> %s </td>" % c)
			files[fn].write("</tr> \n")
			files[fn+'_log'].write("</tr> \n")
			for v in variables:
				files[fn].write("<tr> <td> %s </td> </tr>\n <tr>" % v)
				files[fn+'_log'].write("<tr> <td> %s </td> </tr>\n <tr>" % v)
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpath = "%s/%s_%s_NOMINAL.png" % (mydir, v, fn+c)
					fullpathlog = "%s/%s_%s_NOMINAL_logscale.png" % (mydir, v, fn+c)
					files[fn].write("<td><img src=\"%s\" alt=\"%s\"</img></td>\n" % (fullpath, fullpath))
					files[fn+'_log'].write("<td><img src=\"%s\" alt=\"%s\"</img></td>\n" % (fullpathlog, fullpathlog))
				files[fn].write("</tr> \n")
				files[fn+'_log'].write("</tr> \n")
			files[fn].write("\n </table> \n")
			files[fn+'_log'].write("\n </table> \n")
			files[fn].close()
			files[fn+'_log'].close()

		elif opts.mode == 'VARIABLE':
			for v in variables:
				fn = v+'_'+l
				files[fn] = open(fn+'.html', 'wa')
				files[fn].write("<h1>%s</h1> \n <p> \n" % (fn+" lin scale"))
				files[fn].write("<h2> <a href=\"%s\"> go to log scale </a> </h2> \n <p> \n" % (fn+'_log.html'))
				files[fn+'_log'] = open(fn+'_log.html', 'wa')
				files[fn+'_log'].write("<h1>%s</h1> \n <p> \n" % (fn+" log scale"))
				files[fn+'_log'].write("<h2> <a href=\"%s\"> go to lin scale </a> </h2> \n <p> \n" % (fn+'.html'))
				files[fn].write("<table border=\"1\"> \n <tr> \n")
				files[fn+'_log'].write("<table border=\"1\"> \n <tr> \n")
				for c in channels:
					files[fn].write("<td> %s </td>" % c)
					files[fn+'_log'].write("<td> %s </td>" % c)
				files[fn].write("\n </tr> \n")
				files[fn+'_log'].write("\n </tr> \n")
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpath = "%s/%s_NOMINAL.png" % (mydir, fn+c)
					fullpathlog = "%s/%s_NOMINAL_logscale.png" % (mydir, fn+c)
					files[fn].write("<td><img src=\"%s\" alt=\"%s\"</img></td>\n" % (fullpath, fullpath))
					files[fn+'_log'].write("<td><img src=\"%s\" alt=\"%s\"</img></td>\n" % (fullpathlog, fullpathlog))
				files[fn].write("\n </tr> </table> \n")
				files[fn+'_log'].write("\n </tr> </table> \n")
				files[fn].close()
				files[fn+'_log'].close()
				htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%(fn+'.html', v))
			htmlindex.write('</ul> \n')
	htmlindex.write('</ul> \n')
	htmlindex.close()

#==================== ^_^ ====================#
if __name__=="__main__":
        main()
