import argparse
import logging
import os
import pathlib

from compiler_modules._modules import MODULES

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Kirby's Dream Land 3 Asset Prettifyer")
    parser.add_argument("-r", "--region", choices=("US", "JP"), default="US")
    parser.add_argument("-d", "--debug-level", type=int, default=logging.INFO)
    parser.add_argument("-y", "--yes-to-all", action='store_true')
    parser.add_argument("project_root")
    args = parser.parse_args()
    
    logging.root.setLevel(args.debug_level)
    
    ROMID = "KDL3_U" if args.region == "US" else "KDL3_J"
    
    logging.info(f"Prettifying KDL3 assets at {args.project_root}...")
    
    if os.path.exists(os.path.join(args.project_root, "Pretty")):
        if args.yes_to_all:
            logging.warning("Pretty assets already exist, but -y was passed. Data will be overwritten.")
        else:
            answer = ""
            while answer not in ("y", "n"):
                answer = input("Pretty assets already exist! Data will be overwritten. Continue? [Y/N] >").lower()
            if answer == "n":
                exit(1)
            
    
    pathlib.Path(os.path.join(args.project_root, "Pretty")).mkdir(exist_ok=True)
    
    for module in MODULES:
        moduleObject = module(args.project_root, ROMID)
        moduleObject.toPrettyFormat()
    
    logging.info("Done!")