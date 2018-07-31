# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig_USC
        # Sets initial batch of config options from parent_hecConfig_USC.py
        self = parent_hecConfig_USC.setme1(self)

        # Sets second batch of config options from parent_hecConfig_USC.py
        self.rasProjectName = "Base_and_Calibration"
        self.parent_hecConfig = "parent_hecConfig_USC"
        self = parent_hecConfig_USC.setme2ras(self)

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getRasProjectPath(self):
        return self.rasProjectPath
