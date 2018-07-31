# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig_CalSag
        # Sets initial batch of config options from parent_hecConfig_USC.py
        self = parent_hecConfig_CalSag.setme1(self)

        # Sets second batch of config options from parent_hecConfig_USC.py
        print("+++++++++++++++++++++++++++++++ rasProjectName ++++++++++++++++++++++++++++++")
        self.rasProjectName = "TICR_Baseline"
        self.rasProjectPath = self.modelVersion + ""
        self.parent_hecConfig = "parent_hecConfig_CalSag"
        self = parent_hecConfig_CalSag.setme2ras(self)
        self.hmsProjectName = "TICR_Design"

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getRasProjectPath(self):
        return self.rasProjectPath
