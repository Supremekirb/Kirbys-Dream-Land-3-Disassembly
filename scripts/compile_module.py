import os

class KDL3Module:
    MODULE_NAME = ""
    def __init__(self, projectDir: str, romID: str):
        self.projectDir = projectDir
        self.romID = romID
        
    def toPrettyFormat(self):
        raise NotImplementedError
        
    def fromPrettyFormat(self):
        raise NotImplementedError
    
    @property
    def moduleAssetFolder(self):
        if self.MODULE_NAME:
            return os.path.join(self.prettyPath, self.MODULE_NAME)
        else: return self.prettyPath
        
    @property
    def prettyPath(self):
        return os.path.join(self.projectDir, "Pretty")