import argparse
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Kirby's Dream Land 3 Assembler")
    parser.add_argument("-a", "--asar", default="asar")
    parser.add_argument("-r", "--region", choices=("US", "JP"), default="US")
    parser.add_argument("project_root")
    parser.add_argument("output")
    
    args = parser.parse_args()
    
    ROMID = "KDL3_U" if args.region == "US" else "KDL3_J"

    if os.path.exists(args.output):
        os.remove(args.output)
        
    print(f"ASAR: {args.asar} | REGION: {args.region}")
    print(f"PROJECT {args.project_root} | OUTPUT: {args.output}")
    print(f"Assembling Kirby's Dream Land 3 ({args.region})...")
    
    def StandardAsarRun(filetype, path, output, extra=None):
        arguments = str.split(
            f"{extra+" " if extra else ""}--no-title-check --define GameID=KDL3 --define ROMID={ROMID} --define FileType={filetype} {f"--define PathToFile={path}" if path else ""} {args.project_root}/Global/AssembleFile.asm {output}"
        )
        subprocess.run(
            (args.asar, *arguments))
    
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