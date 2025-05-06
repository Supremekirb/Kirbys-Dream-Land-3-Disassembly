import argparse
import os
import subprocess

from modules import MODULES

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Kirby's Dream Land 3 Project Compiler")
    parser.add_argument("-a", "--asar", default="asar")
    parser.add_argument("-r", "--region", choices=("US", "JP"), default="US")
    parser.add_argument("project_root")
    parser.add_argument("output")
    args = parser.parse_args()
    
    ROMID = "KDL3_U" if args.region == "US" else "KDL3_J"
    
    print("KIRBY'S DREAM LAND 3 PROJECT COMPILER")
    print(f"ASAR: {args.asar} | REGION: {args.region}")
    print(f"PROJECT {args.project_root} | OUTPUT: {args.output}")
    
    print("Converting pretty files...")
    for module in   MODULES:
        moduleObject = module(args.project_root, ROMID)
        moduleObject.fromPrettyFormat()
    
    # stuff from here on is based on the batch script
    print(f"Assembling Kirby's Dream Land 3 ({args.region})...")
    if os.path.exists(args.output):
        os.rename(args.output, args.output + "_TEMP_BACKUP")
    
    def StandardAsarRun(filetype, path, output, extra=None):
        arguments = str.split(
            f"{extra+" " if extra else ""}--no-title-check --define GameID=KDL3 --define ROMID={ROMID} --define FileType={filetype} {f"--define PathToFile={path}" if path else ""} {args.project_root}/Global/AssembleFile.asm {output}"
        )
        result = subprocess.run(
            (args.asar, *arguments))
        try:
            result.check_returncode()
        except subprocess.CalledProcessError:
            os.remove(args.output)
            if os.path.exists(args.output + "_TEMP_BACKUP"):
                os.rename(args.output + "_TEMP_BACKUP", args.output)
            raise
    
    StandardAsarRun(0, None, args.output, "--fix-checksum=on")

    print("Assembling sound engine...")
    StandardAsarRun(4, f"{args.project_root}/KDL3/SPC700/Engine.asm", f"{args.project_root}/KDL3/SPC700/Engine.bin")
    StandardAsarRun(4, f"{args.project_root}/KDL3/SPC700/GlobalSampleBank.asm", f"{args.project_root}/KDL3/SPC700/GlobalSampleBank.bin")
    for i in range(0, 10):
        StandardAsarRun(
            4, f"{args.project_root}/KDL3/SPC700/LocalSampleBank0{i}.asm", f"{args.project_root}/KDL3/SPC700/LocalSampleBank0{i}.bin"
        )
        
    print("Assembling ROM...")
    StandardAsarRun(1, None, args.output)
    
    if os.path.exists(f"{args.project_root}/KDL3/Temp.txt"):
        os.remove(f"{args.project_root}/KDL3/Temp.txt")
        
    StandardAsarRun(2, None, args.output)
    StandardAsarRun(3, None, args.output, "--fix-checksum=off")
    
    
    print("Done!")