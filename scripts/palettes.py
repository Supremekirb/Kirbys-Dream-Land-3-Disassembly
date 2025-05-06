import glob
import logging
import os
import pathlib

import palette_converter
from compile_module import KDL3Module


class PalettesModule(KDL3Module):
    MODULE_NAME = "Palettes"
    def toPrettyFormat(self):
        logging.info("Reformatting palettes...")
        
        pathlib.Path(self.moduleAssetFolder).mkdir(exist_ok=True)
        
        for file in glob.glob(os.path.join(self.projectDir, "KDL3/Palettes/*.bin")):
            path = os.path.join(self.moduleAssetFolder, os.path.splitext(os.path.basename(file))[0] + ".pal")
            with open(file, "rb") as input, open(path, "w") as output:
                logging.debug(f"Converting palette {file}...")
                # right now, uses Jasc palettes always. Might change this later
                palette_converter.binaryToJascPal(input, output)
                
        logging.info("Reformatted palettes!")
        
    def fromPrettyFormat(self):
        ...