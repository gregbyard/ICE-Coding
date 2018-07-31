#!/usr/bin/python

import os,json,sys,shutil
import runModel,SplitBasins.InitHMS

#subhms = open("CalSag_hms.txt").readlines()
#subhms = open("Poplar_hms.txt").readlines()
subhms = open("USC_hms.txt").readlines()
#subhms = sys.stdin.readlines()
subhms = runModel.stripLines(subhms)

for s in subhms:
    print(s + str(len(subhms)) + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    runModel.rmCompiled()
    # rename config file for use in scripts
    backupFileName = s + "_hmsConfig.py"

    # obtain configuration details for HEC applications for
    # python and jython scripts
    config = runModel.parent_config(backupFileName)
    curdir = os.getcwd()
    print(curdir)
    os.chdir(config.scriptPath)
    #print(vars(config))

    # Split subbasins and assign future properties
    print("Creating redeveloped subbasins...")
    SplitBasins.InitHMS.main(config)

    swStructure = json.load(open(config.inputFileName, 'rb'))
    subbasins = swStructure['subbasins']
    #ditchNames = swStructure['ditchNames']
    print("Input file name: " + config.inputFileName)
    print(subbasins)

    # Obtain instance of our HEC "model"
    #from hecModel import Model
    #model = Model()
    import hecModel
    from hecModel import Model
    reload(hecModel)
    model = Model()

    # Create dummy storage-outflow curves
    print("new curves")
    model.newStorageOutflowCurves()

    # Run HEC-HMS model
    print("Running HEC-HMS the first time...")
    model.runHms()

    # Build storage curves
    # Create for a 24h storm or copy for a 12h storm
    # The 24h storm must run before the 12h storm
    if "12" in config.hmsRunName:
        print("Copying storage-outflow curves...")
        model.copyStorageOutflowCurves(subbasins)
    elif "24" in config.hmsRunName:
        print("Creating storage-outflow curves...")
        model.createStorageOutflowCurves(subbasins)
    else:
        print("Can't tell if 12h or 24h precipitation.")

    # run HEC-HMS model
    print("Running HEC-HMS the second time...")
    model.runHms()
