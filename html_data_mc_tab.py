#!/usr/bin/env python

###############################
# a.succurro ATgmail.com # 2011 #
###############################

# python script to produce .html files
# showing plots of interest
# in an ordered format

import os, sys
from sys import stdout
import fileinput


finName1=sys.argv[1]
foutName1 = finName1+".html"

try:
        fout = open(foutName1, 'wa')
except IOError:
        print "cannot open file" , foutName1

varName = []
fullLine = []

#optStudies_regionA_merged_true_h1_pT_LjLj_ttbar_cut1.png
for lineFile in fileinput.input(finName1+".txt"):
        splittedLine = lineFile.split("_")
        namevar = splittedLine[0]
        if "Wlep" in splittedLine[0] or "JetPtB" in splittedLine[0]  or "Whad" in splittedLine[0]:
                namevar = splittedLine[0]+" "+splittedLine[1]
        elif "deltaR" in splittedLine[0]:
                namevar= splittedLine[0]+" "+splittedLine[1]+" "+splittedLine[2]
        varName.append(namevar)
        fullLine.append(lineFile)
        

for variable,lineFile in zip(varName,fullLine):
        fout.write("<h1>%s</h1> \n <p> \n" % variable)
        ##fout.write("<table border=\"1\"> \n <tr> \n <td> 4jet0tagex </td> <td> 4jet1tagex HT < 700GeV </td><td> 4jet1tagex m(jjj) < 350GeV</td><td> 4jet2tagin HT < 700GeV </td><td> 4jet2tagin m(jjj) < 350GeV</td><td> CH1+CH2 DR cuts reversed </td><td> CH3 DR cuts reversed </td><td> CH1+CH2 DR cuts reversed HT cut dropped</td><td> CH3 DR cuts reversed  HT cut dropped</td><td> CH1+CH2 DR cuts reversed bjet pt cut dropped</td><td> CH3 DR cuts reversed  bjet pt cut dropped</td><td> CH1+CH2 DR cuts reversed DR(lep,nu) cut dropped</td><td> CH3 DR cuts reversed  DR(lep,nu) cut dropped</td><td> CH1+CH2 loose </td><td> CH3 loose </td> <td> CH1+CH2 tight </td><td> CH3 tight </td> \n </tr> <tr> \n")
        fout.write("<table border=\"1\"> \n <tr> \n <td> 4jet0tagex  </td><td> 4jet1tagin HT < 700GeV </td><td> 4jet1tagin m(jjj) < 350GeV</td> <td> CH1+CH2 DR cuts reversed </td><td> CH3 DR cuts reversed </td><td> CH1+CH2 DR cuts reversed HT cut dropped</td><td> CH3 DR cuts reversed  HT cut dropped</td><td> CH1+CH2 DR cuts reversed bjet pt cut dropped</td><td> CH3 DR cuts reversed  bjet pt cut dropped</td><td> CH1+CH2 DR cuts reversed DR(lep,nu) cut dropped</td><td> CH3 DR cuts reversed  DR(lep,nu) cut dropped</td><td> CH1 loose </td><td> CH2 loose </td><td> CH1+CH2 loose </td><td> CH3 loose </td> <td> CH1 tight </td> <td> CH2 tight </td> <td> CH1+CH2 tight </td><td> CH3 tight </td> \n </tr> <tr> \n")
        splittedLine = lineFile.split("_")
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
        ch2=var+"_"+lep+"_4jet1tagexHT_"+nom
        ch3=var+"_"+lep+"_4jet1tagexMjjj_"+nom
                #ch4=var+"_"+lep+"_4jet2taginHT_"+nom
                #ch5=var+"_"+lep+"_4jet2taginMjjj_"+nom
        ch4=var+"_"+lep+"_4jet1taginHT_"+nom
        ch5=var+"_"+lep+"_4jet1taginMjjj_"+nom
        ch6=var+"_"+lep+"u4u4rev_CH1plusCH2_"+nom
        ch7=var+"_"+lep+"u4u4rev_CH3_"+nom
        ch12=var+"_"+lep+"u4u4revCRa_CH1plusCH2_"+nom
        ch13=var+"_"+lep+"u4u4revCRa_CH3_"+nom
        ch14=var+"_"+lep+"u4u4revCRb_CH1plusCH2_"+nom
        ch15=var+"_"+lep+"u4u4revCRb_CH3_"+nom
        ch16=var+"_"+lep+"u4u4revCRc_CH1plusCH2_"+nom
        ch17=var+"_"+lep+"u4u4revCRc_CH3_"+nom
        ch18=var+"_"+lep+"u4u4_CH1_"+nom
        ch19=var+"_"+lep+"u4u4_CH2_"+nom
        ch8=var+"_"+lep+"u4u4_CH1plusCH2_"+nom
        ch9=var+"_"+lep+"u4u4_CH3_"+nom
        ch20=var+"_"+lep+"u4u4tight_CH1_"+nom
        ch21=var+"_"+lep+"u4u4tight_CH2_"+nom
        ch10=var+"_"+lep+"u4u4tight_CH1plusCH2_"+nom
        ch11=var+"_"+lep+"u4u4tight_CH3_"+nom
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (lineFile, lineFile))
                        #fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch2, ch2))
                        #fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch3, ch3))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch4, ch4))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch5, ch5))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch6, ch6))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch7, ch7))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch12, ch12))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch13, ch13))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch14, ch14))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch15, ch15))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch16, ch16))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch17, ch17))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch18, ch18))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch19, ch19))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch8, ch8))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch9, ch9))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch20, ch20))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch21, ch21))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch10, ch10))
        fout.write("<td><img src=\"%s\" alt=\"%s\"</img> </td>\n" % (ch11, ch11))
        fout.write("</tr> </table> </p> <br> \n")
fout.write("</body> \n </html>")

fout.close()

