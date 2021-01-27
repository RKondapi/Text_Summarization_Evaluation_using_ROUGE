# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import rouge
import os
import gc
import datetime
starttime = datetime.datetime.now()
def prepare_results(p, r, f):
    return '\t{}:\t{}: {:5.2f}\t{}: {:5.2f}\t{}: {:5.2f}'.format(metric, 'P', 100.0 * p, 'R', 100.0 * r, 'F1', 100.0 * f)

evaluator=rouge.Rouge(metrics=['rouge-n', 'rouge-l'],
                       max_n=2,
                       limit_length=True,
                       length_limit=100,
                       length_limit_type='words',
                       apply_avg=apply_avg,
                       apply_best=apply_best,
                       alpha=0.5, # Default F1_score
                       weight_factor=1.2,
                       stemming=True)

sytemFileNames=[]
def getSysSummaries(systemPath):
    systemTexts=[]
    dirc=os.listdir(systemPath)
    for files in dirc:
        f=systemPath+'/'+files
        sytemFileNames.append(files.split('t')[0].upper())
        with open(f, encoding = "utf-8", errors = 'ignore') as file:
                systemTexts.append(file.read())
                file.close()
        gc.collect()
    return systemTexts
def getHumanSummaries(humanPath):
    humanTextsTemp=[]
    dirc=os.listdir(humanPath)
    humanFileNames=[]
    humanTexts=[]
    for files in dirc:
        if any(substring in files for substring in sytemFileNames):
            f=humanPath+'/'+files
            humanFileNames.append(files.split('.')[0])
            with open(f, encoding = "utf-8", errors = 'ignore') as file:
                    humanTextsTemp.append(file.read())
                    file.close()
            gc.collect()
    humanTexts=[humanTextsTemp[i:i+4] for i in range(0,len(humanTextsTemp),4)]
    return humanTexts
system=["Centroid","DPP","ICSISumm","LexRank","Submodular"]
systemPath=input("Enter the path of system summaries (till the 'System_Summaries' folder):\n")
#systemPath="D:\HW3\HW3\System_Summaries"
humanPath=input("Enter the path of human summaries (till the 'eval' folder):\n")
#humanPath="D:\HW3\HW3\Human_Summaries\eval"
for eachSystem in system:
    print("\nFor "+eachSystem+":")
    systemTexts=getSysSummaries(systemPath+"\\"+eachSystem)
    humanTexts=getHumanSummaries(humanPath)
    scores = evaluator.get_scores(systemTexts,humanTexts)

    for metric, results in sorted(scores.items(), key=lambda x: x[0]):
        print(prepare_results(results['p'], results['r'], results['f']))

endtime = datetime.datetime.now()
print("Total Execution Time in HH:MM:SS Format:", endtime-starttime)