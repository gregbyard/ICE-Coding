# Simple python class for a constant configuration
# that is used through all HEC Python/Jython scripts

class HecConfig:
    """Simple class maintaining configuration for HEC applications"""
    def __init__(self):
        import parent_hecConfig_Poplar
        # Sets initial batch of config options from parent_hecConfig_USC.py
        self = parent_hecConfig_Poplar.setme1(self)

        # Name of directory that contains the model versions
        self.hmsProjectPath = self.modelVersion + "HEC-HMS/PC_Schaumburg/"
        #self.osHmsProjectPath = self.osHmsVersion + "HMS/"
        #self.rasProjectPath = self.modelVersion + "RAS/PCEB/"
        self.hmsProjectName = "PC_Schaumburg"
        self.parent_hecConfig = "parent_hecConfig_Poplar"
        self.basinin = self.hmsProjectPath + "/PCSH_Exist.basin.backup"
        self.basinout = self.hmsProjectPath + "/PCSH_Exist.basin"

        # Sets second batch of config options from parent_hecConfig_USC.py
        self = parent_hecConfig_Poplar.setme2hms(self)

    def getDataTransferFilePath(self):
        return self.scriptPath + "/jythonDtf.txt"

    def getHmsProjectPath(self):
        return self.hmsProjectPath

    def getHmsProjectName(self):
        return self.hmsProjectName
