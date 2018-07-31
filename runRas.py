#!/usr/bin/python

import os,sys
import runModel,hecModel

#subras = open("CalSag_ras.txt").readlines()
subras = open("Poplar_ras.txt").readlines()
subras = open("USC_ras.txt").readlines()
#subras = sys.stdin.readlines()
subras = runModel.stripLines(subras)

# Run HEC-RAS model
for s in subras:
    print(s + str(len(subras)) + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print(os.getcwd())
    runModel.rmCompiled()
    # get config for this RAS run
    backupFileName = s + "_rasConfig.py"
    #print(backupFileName)
    config = runModel.parent_config(backupFileName)
    #print(vars(config))
    reload(hecModel)
    # create new Model object
    model = hecModel.Model()
    # run RAS model
    model.runRas()
