#!/usr/bin/env python

###############################
# a.succurro@gmail.com # 2011 #
###############################

# python script to produce .tex files
# as input for beamer files
# with the plots of interest


import os, sys
from sys import stdout
import fileinput


finName1=sys.argv[1]
foutpath="/home/succurro/Documents/Physics/talks/u4u4/20120528exotics/"

channels = ["_4jet0tagex", "_4jet1taginHT", "_4jet1taginMjjj",  "u4u4rev_CH1plusCH2", "u4u4rev_CH3", "u4u4_CH1plusCH2", "u4u4_CH3", "u4u4tight_CH1plusCH2", "u4u4tight_CH3", "u4u4revCRa_CH1plusCH2", "u4u4revCRa_CH3", "u4u4revCRb_CH1plusCH2", "u4u4revCRb_CH3", "u4u4revCRc_CH1plusCH2", "u4u4revCRc_CH3"]

foutName = []
fout = []

chN = len(channels)

for i in range(chN):
        foutName.append(foutpath+finName1+channels[i]+".tex")
        fout.append(open(foutName[i], 'wa'))

lepton = "muon"
if "ELE" in finName1:
        if "MUON" in finName1:
                lepton = "ele+muon"
        else:
                lepton = "electron"

varName = []
basepath = "../../../plots/20120528_datamc_ICHEP/"

#optStudies_regionA_merged_true_h1_pT_LjLj_ttbar_cut1.png
for lineFile in fileinput.input(finName1+".txt"):
        splittedLine = lineFile.split("_")
        varName.append(splittedLine[0])
        #channel = splittedLine[2]



fout[0].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "4jet0tagex" ) )
fout[1].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "4jet1tagin HT $ < $ 700GeV" ) )
fout[2].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "4jet1tagin mchi2  $ < $ 350GeV" ) )
fout[3].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 reversed DRcut" ) )
fout[4].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 reversed DRcut" ) )
fout[5].write("\\begin{frame}\\frametitle{ MC expectation %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 loose" ) )
fout[6].write("\\begin{frame}\\frametitle{ MC expectation %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 loose" ) )
fout[7].write("\\begin{frame}\\frametitle{ MC expectation %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 tight" ) )
fout[8].write("\\begin{frame}\\frametitle{ MC expectation %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 tight" ) )
fout[9].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 reversed DRcut, HT cut dropped" ) )
fout[10].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 reversed DRcut, HT cut dropped" ) )
fout[11].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 reversed DRcut, bjet pt cut dropped" ) )
fout[12].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 reversed DRcut, bjet pt cut dropped" ) )
fout[13].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH1+CH2 reversed DRcut, DR(lep,nu) cut dropped" ) )
fout[14].write("\\begin{frame}\\frametitle{ Data/MC %s %s }\n \\small \\centering \n\n" % (lepton, "CH3 reversed DRcut, DR(lep,nu) cut dropped" ) )



count = 0
for lineFile in fileinput.input(finName1+".txt"):
        count +=1
        lineFile= lineFile.rstrip().lstrip()
        splittedLine = lineFile.split("_") #0tagex
        if "Wlep" in splittedLine[0] or "JetPtB" in splittedLine[0] or "Whad" in splittedLine[0]:
                var = splittedLine[0]+"_"+splittedLine[1]
                lep = splittedLine[2]
                nom = splittedLine[4]
        elif "deltaR" in splittedLine[0]:
                var = splittedLine[0]+"_"+splittedLine[1]+"_"+splittedLine[2]
                lep = splittedLine[3]
                nom = splittedLine[5]
        else:
                var = splittedLine[0]
                lep = splittedLine[1]
                nom = splittedLine[3]

        for i in range(chN):
                name = var+"_"+lep+channels[i]+"_"+nom
                if len(varName)>4:
                        fout[i].write("\\includegraphics[width=.3\\textwidth, height=.4\\textheight]{%s%s}" % (basepath, name))
                        if count is 3:
                                fout[i].write("\\\\  \n\\centering\n")
                else:
                        fout[i].write("\\includegraphics[width=.4\\textwidth, height=.4\\textheight]{%s%s}" % (basepath, name))
                        if count is 2:
                                fout[i].write("\\\\  \n\\centering\n")

for i in range(chN):
        fout[i].write("\n\n\\end{frame}\n\n")
        fout[i].close()

