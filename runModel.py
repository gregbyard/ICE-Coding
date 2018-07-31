#!/usr/bin/python
# Script to execute the ISWS HEC-HMS and HEC-RAS model

import os,shutil,glob

def stripLines(filecontents):
    filecontents = [line.rstrip('\r\n') for line in filecontents]
    return filecontents


def rmCompiled():
    try:
        print("Removing *.pyc and *$py.class.")
        print(glob.glob("*.pyc"))
        for f in glob.glob("*.pyc"):
            os.remove(f)
        for f in glob.glob("*$py.class"):
            os.remove(f)
    except Exception, e:
        print("No *.pyc or *$py.class to remove.")


def parent_config(hecConfig):
    # obtain configuration details for HEC applications for
    # python and jython scripts
    # try:
    #     os.remove("hecConfig.pyc")
    #     os.remove("hecConfig$py.class")
    # except Exception, e:
    #     print("hecConfig.pyc or hecConfig$py.class does not yet exist.")
    rmCompiled()
    shutil.copyfile(hecConfig, "hecConfig.py")
    import hecConfig
    reload(hecConfig)
    config = hecConfig.HecConfig()
    try:
        os.remove(config.modelVersion + config.parent_hecConfig + ".py")
    except Exception, e:
        print(config.parent_hecConfig + ".py has never been copied for this model version.")
    shutil.copyfile(config.parent_hecConfig + ".py", config.modelVersion + config.parent_hecConfig + ".py")
    return config
