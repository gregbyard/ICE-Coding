# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig_Poplar
        # Sets initial batch of config options from parent_hecConfig_USC.py
        self = parent_hecConfig_Poplar.setme1(self)

        # Sets second batch of config options from parent_hecConfig_USC.py
        print("+++++++++++++++++++++++++++++++ rasProjectName ++++++++++++++++++++++++++++++")
        self.rasProjectName = "PCRR"
        self.rasProjectPath = self.modelVersion + "RAS/PCRR"
        self.parent_hecConfig = "parent_hecConfig_Poplar"
        self = parent_hecConfig_Poplar.setme2ras(self)

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getRasProjectPath(self):
        return self.rasProjectPath
