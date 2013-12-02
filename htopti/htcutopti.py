#! /bin/env python
#==================== ^_^ ====================#
# succurro@ifae.es
# use yield dictionaries from compareyields
# to fill latex tables
#==================== ^_^ ====================#
import os, sys
from sys import stdout
sys.path.append('/nfs/at3users/users/succurro/05histogrammer/AnaTools/MVA/FinalTreeMaker/myscripts/')
import fileinput
import commands
#import argparse
import optparse
import math as math
from array import array
#from namings import thecutsname, thesamplesname
import rootlogon
import ROOT

ROOT.gROOT.SetStyle("ATLAS")
#ROOT.gROOT.ForceStyle()
ROOT.gStyle.SetOptTitle(0)
#TGaxis.SetMaxDigits(4)
ROOT.gErrorIgnoreLevel = 1001
ROOT.gROOT.SetBatch(1)

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


basepath = "/nfs/at3/scratch2/succurro/FinalHistMCLimit_vlq/limitfiles/"
outpath = basepath

yieldsdict = {}
thesignal = "VLT"

sampcolors = {
    "BKGS_5200": ["MC@NLO", 1],
    "BKGS_5860_fast": ["PowHer", 3],
    "BKGS_117050": ["PowPy full rew", 4],
    "BKGS_117050_fast": ["PowPy fast rew", 2],
    "BKGS_117050_fast_noREW": ["PowPy fast", 6],
    "BKGS_117050_noREW": ["PowPy full", 7],
    "BKGS_Alpgen_HFOR": ["Alpgen", 5],
    }

#==================== ^_^ ====================#
def options():
        '''define here in-line arguments'''
        #parser = argparse.ArgumentParser(description='I do nice things with the right inputs!')
        #parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        parser = optparse.OptionParser(description='I do nice things with the right inputs!')
        parser.add_option("-v", "--verbose", dest='verbose', help="increase output verbosity", action="store_true")
	parser.add_option("-d", "--inputdir", dest='inputdir', help="input dir for the files", default="mydir")
	parser.add_option("-s", "--samples", dest='samples', help="samples to run on")
	parser.add_option("-l", "--listsys", dest='listsys', help="list of systematics to run on", default="NOMINAL")
	parser.add_option("-b", "--btagmode", dest='btagmode', help="choose Cut or TRF", default="Cut")
	parser.add_option("-c", "--channels", dest='channels', help="channels to run on", default="4jetin0btagin")
	parser.add_option("-L", "--Lep", dest='Lep', help="lepton channel: ELE MUON ELEMUON", default="ELEMUON")
	parser.add_option("-I", "--Interactivemode", dest='Interactivemode', help="will prompt for inputs", action="store_true")
	parser.add_option("-y", "--isyields", dest='isyields', help="will report yields instead of entries", action="store_true")
	parser.add_option("-e", "--showEff", dest='showEff', help="adds a column with cut efficiency", action="store_true")
	parser.add_option("-g", "--showGain", dest='showGain', help="adds a column with percentage of events gain", action="store_true")
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

	thesamples = opts.samples.split(' ')
	thesys     = opts.listsys.split(' ')[0]
	thechannels= opts.channels.split(' ')

	for s in thesamples:
		yieldsdict[s] = getattr(__import__(s+"_"+thesys), s)

	plotRatios(opts.Lep, thesamples, thechannels, opts.showEff, opts.isyields, opts.verbose)

def plotRatios(l, thesamples, thechannels, showEff, isyields, verbose):
	ratios = {}
	errors = {}
	bkgs = []
	for s in thesamples:
		if s != "Data":
			bkgs.append(s)
			rr = []
			ee = []
			for c in thechannels:
				rr.append(yieldsdict["Data"][l+c][0]/yieldsdict[s][l+c][0])
				err = (yieldsdict[s][l+c][1]/yieldsdict[s][l+c][0])**2 \
				      + (yieldsdict["Data"][l+c][1]/yieldsdict["Data"][l+c][0])**2
				ee.append(math.sqrt(err))
			ratios[s] = array( 'd', rr)
			errors[s] = array( 'd', ee)

	yerr = []
	ypsilons={}
	n = len(bkgs)
	for b in range(n):
		ypsilons[bkgs[b]] = []
		for c in thechannels:
			i = int(sdrnaming[c][3:])
			ypsilons[bkgs[b]].append(i+(0.8*b/n))
			print bkgs[b]," in channel ",c," has Y=",(i+(0.8*b/n))
		yerr.append(0)
	yaxis = []
	for b in bkgs:
		yaxis.append(array('d', ypsilons[b]))
	yerr = array('d', yerr)

        thelegend = ROOT.TLegend(0.2, 0.8, 0.5, 0.95 )
        thelegend.SetFillStyle(0)
        thelegend.SetLineColor(0)
        thelegend.SetBorderSize(0)
        thelegend.SetShadowColor(10)

	graphratio = []
	for i in range(n):
		graphratio.append( ROOT.TGraphErrors(len(ratios[bkgs[i]]), ratios[bkgs[i]], yaxis[i], errors[bkgs[i]], yerr) )
		graphratio[i].SetLineStyle(1)
		graphratio[i].SetLineWidth(3)
		graphratio[i].SetLineColor(sampcolors[bkgs[i]][1])
		graphratio[i].SetMarkerColor(sampcolors[bkgs[i]][1])
		thelegend.AddEntry(graphratio[i], sampcolors[bkgs[i]][0],'l')
        thecanvas = ROOT.TCanvas("thecanvas", "thecanvas", 600, 600 )
        thecanvas.cd()
	thecanvas.SetTopMargin(0.036) ###margin goes to the top of the pad
	thecanvas.SetBottomMargin(0.104) ###low margin goes to the bottom
	thecanvas.SetLeftMargin(0.15)
	thecanvas.SetRightMargin(0.05)
        #thecanvas.SetRightMargin(0.08)
	dummy = ROOT.TH1F("dummy", "dummy", 10, 0., 2.)
	dummy.GetXaxis().SetTitle("Data/MC")
	dummy.GetYaxis().SetTitle("SDR")
	ymax = 1.5*len(thechannels)
	dummy.SetMaximum(ymax)
	dummy.SetMinimum(0.)
	dummy.GetXaxis().SetLabelFont(43)
	dummy.GetXaxis().SetLabelSize(20) ###labels will be 16 pixels
	dummy.GetYaxis().SetLabelFont(43)
	dummy.GetYaxis().SetLabelSize(20) ###labels will be 16 pixels
	dummy.GetXaxis().SetTitleFont(43)
	dummy.GetXaxis().SetTitleSize(25)
	dummy.GetYaxis().SetTitleFont(43)
	dummy.GetYaxis().SetTitleSize(20) ###labels will be 16 pixels
	dummy.GetYaxis().SetTitleOffset(1.5)
	dummy.Draw()
	line = ROOT.TLine(1.,0.,1.,ymax)
	line.SetLineColor(2)
	line.SetLineStyle(2)
	chlines = []
	for i in range(len(thechannels)):
		ll = ROOT.TLine(0.,i+1.,2.,i+1.)
		ll.SetLineStyle(2)
		chlines.append(ll)
	
	for i in range(n):
		graphratio[i].Draw("P same")
	thelegend.Draw()
	line.Draw("same")
	for ll in chlines:
		ll.Draw("same")
        # "  #sqrt{s} = 8 TeV")
	atlasTex = ROOT.TLatex(0.40,0.88,"ATLAS")
	atlasTex2 = ROOT.TLatex(0.40,0.88,"              Internal")
	atlasTex.SetNDC()
	atlasTex.SetTextFont(72)
	atlasTex.SetTextSize(0.04)
	atlasTex.SetLineWidth(2)
	#atlasTex.Draw()
	atlasTex2.SetNDC()
	atlasTex2.SetTextFont(42)
	atlasTex2.SetTextSize(0.04)
	atlasTex2.SetLineWidth(2)
	#atlasTex2.Draw("same")
	#thecanvas.RedrawAxis()
	    
	thecanvas.Update()
	thecanvas.Modified()
	thecanvas.SaveAs("../plots/datamcsummary_"+l+".png")
	thecanvas.SaveAs("../plots/datamcsummary_"+l+".eps")

	

#__________________________________________________________

if __name__=="__main__":
	main()
