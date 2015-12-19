#!/usr/bin/env python

###############################
# a.succurro ATgmail.com # 2013 #
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

sdrnaming = {
	'CR0_1W': 'SDR0',
	'CR1_1W': 'SDR2',
	'CR2_1W': 'SDR3',
	'CR3_1W': 'SDR4',
	'CR4_1W': 'SDR5',
	'CR5_1W': 'SDR1',
	'CR6_1W': 'SDR6',
	'CR7_1W': 'SDR7',
	'CR8_1W': 'SDR8',
	'CR9_1W': 'SDR9',
	'CR10_1W': 'CR10',
	'CR11_1W': 'CR11',
}

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

def insertimg(imgpath):
	return "<a href=\"%s\"><img src=\"%s\" alt=\"%s\"</img></a>" % (imgpath, imgpath, imgpath)


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
				htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%
						(fn+'_'+opts.inputdir+'.html', sdrnaming.get(c, c.replace('_',' '))))
				files[fn] = open(fn+'_'+opts.inputdir+'.html', 'wa')
				files[fn].write("<h1>%s</h1> \n <p> \n" % (l+' '+sdrnaming.get(c, c)))
				files[fn].write("<table border=\"1\"> \n")
				for v in variables:
					fullpath = "%s/%s_%s_NOMINAL.png" % (mydir, v, fn)
					fullpathlog = "%s/%s_%s_NOMINAL_logscale.png" % (mydir, v, fn)
					files[fn].write("<tr> <td> %s </td>\n" % v)
					files[fn].write("<tr><td>%s</td><td>%s</td></tr>\n" % (insertimg(fullpath), insertimg(fullpathlog)))
				files[fn].write("\n </table> \n")
				files[fn].close()
			htmlindex.write('</ul>\n')

		elif opts.mode == 'ALL':
			fn = l
			htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%(fn+'_'+opts.inputdir+'.html', fn))
			files[fn] = open(fn+'_'+opts.inputdir+'.html', 'wa')
			files[fn].write("<h1>%s</h1> \n <p> \n" % (fn))
			files[fn].write("<table border=\"1\">\n <tr>\n")
			for c in channels:
				files[fn].write("<td> %s </td>" % sdrnaming.get(c, c))
			files[fn].write("</tr> \n")
			for v in variables:
				files[fn].write("<tr> <td> %s linear scale </td> </tr>\n <tr>" % v)
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpath = "%s/%s_%s_NOMINAL.png" % (mydir, v, fn+c)
					files[fn].write("<td>%s</td>\n" % (insertimg(fullpath)))
				files[fn].write("</tr> \n")
				files[fn].write("<tr> <td> %s log scale </td> </tr>\n <tr>" % v)
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpathlog = "%s/%s_%s_NOMINAL_logscale.png" % (mydir, v, fn+c)
					files[fn].write("<td>%s</td>\n" % (insertimg(fullpathlog)))
				files[fn].write("</tr> \n")
			files[fn].write("\n </table> \n")
			files[fn].close()
			htmlindex.write('</ul>\n')

		elif opts.mode == 'VARIABLE':
			for v in variables:
				fn = v+'_'+l
				files[fn] = open(fn+'_'+opts.inputdir+'.html', 'wa')
				files[fn].write("<h1>%s</h1> \n <p> \n" % (fn))
				files[fn].write("<table border=\"1\"> \n <tr> \n")
				for c in channels:
					files[fn].write("<td> %s </td>" % sdrnaming.get(c, c))
				files[fn].write("\n </tr> \n <tr> \n")
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpath = "%s/%s_NOMINAL.png" % (mydir, fn+c)
					files[fn].write("<td>%s</td>\n" % (insertimg(fullpath)))
				files[fn].write("\n </tr> \n <tr> \n")
				for c in channels:
					mydir = getDir(opts.inputdir, l, c)
					fullpathlog = "%s/%s_NOMINAL_logscale.png" % (mydir, fn+c)
					files[fn].write("<td>%s</td>\n" % (insertimg(fullpathlog)))
				files[fn].write("\n </tr> </table> \n")
				files[fn].close()
				htmlindex.write('<li><a href=\"%s\">%s</a></li>\n'%(fn+'_'+opts.inputdir+'.html', v))
			htmlindex.write('</ul> \n')
	htmlindex.write('</ul> \n')
	htmlindex.close()

#==================== ^_^ ====================#
if __name__=="__main__":
        main()
