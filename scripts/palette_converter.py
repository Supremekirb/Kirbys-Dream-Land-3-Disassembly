import argparse
import io
import os


def fromBGR555(colour: int) -> tuple[int, int, int]:
    r = colour & 0b11111
    g = (colour & 0b1111100000) >> 5
    b = (colour & 0b111110000000000) >> 10
    return r*8, g*8, b*8


def toBGR555(rgb: tuple[int, int, int]) -> int:
    r = rgb[0] >> 3
    g = rgb[1] >> 3
    b = rgb[2] >> 3
    return ((b << 10) | (g << 5) | r)


def binToRGBs(input: io.BufferedReader, addTransparentColour = False):
    rgbs: list[tuple[int, int, int]] = []
    if addTransparentColour:
        rgbs.append((0, 0, 0))
    while i:=input.read(2):
        assert len(i) == 2, "Input file is not a multiple of 2 bytes in size!"
        rgbs.append(fromBGR555(int.from_bytes(i, "little")))
    return rgbs


def RGBsToBin(rgbs: list[tuple[int, int, int]], output: io.BufferedWriter):
    for colour in rgbs:
        bgr555 = toBGR555(colour)
        output.write(bgr555.to_bytes(2, 'little'))


def binaryToJascPal(input: io.BufferedReader, output: io.TextIOWrapper, addTransparentColour = False):
    rgbs = binToRGBs(input, addTransparentColour)
    # this header stuff was copied from an example palette file /shrug
    output.write("JASC-PAL\n")
    output.write("0100\n") # length in hex +1? No? Can't figure out what this is
    output.write(f"{len(rgbs)}\n")
    for r, g, b in rgbs:
        output.write(str(r) + " ")
        output.write(str(g) + " ")
        output.write(str(b) + "\n")
        
        
def jascPalToBinary(input: io.TextIOWrapper, output: io.BufferedWriter, addTransparentColour = False):
    rgbs: list[tuple[int, int, int]] = []
    
    if addTransparentColour:
        rgbs.append((0, 0, 0))
        
    for i in input.readlines():
        split = i.split()
        if len(split) == 3:
            rgbs.append(tuple(int(channel) for channel in split))
    
    RGBsToBin(rgbs, output)
            

def binaryToMSPal(input: io.BufferedReader, output: io.BufferedWriter, addTransparentColour = False):
    rgbs = binToRGBs(input, addTransparentColour)
    header_size = len("RIFF") + 4 + len("PAL data") + 4 + 2 + 2 # 24 bytes
    file_size = header_size + len(rgbs)*4

    output.write(bytes("RIFF", encoding="ASCII"))
    output.write((file_size-8).to_bytes(4, "little"))
    output.write(bytes("PAL data", encoding="ASCII"))
    output.write((file_size-20).to_bytes(4, "little"))
    output.write((0).to_bytes(1))
    output.write((3).to_bytes(1))
    output.write((len(rgbs)).to_bytes(2, "little"))

    for r, g, b in rgbs:
        output.write(r.to_bytes(1))
        output.write(g.to_bytes(1))
        output.write(b.to_bytes(1))
        output.write((0).to_bytes(1))


def MSPalToBinary(input: io.BufferedReader, output: io.BufferedWriter, addTransparentColour = False):
    # untested lol
    rgbs: list[tuple[int, int, int]] = []
    
    if addTransparentColour:
        rgbs.append((0, 0, 0))

    input.seek(len("RIFF") + 4 + len("PAL data") + 4 + 2 + 2) # header size, 24 bytes
    while i:=input.read(4):
        assert len(i) == 4, "Input file not a multiple of 4 bytes in size!"
        rgbs.append(tuple(i[channel] for channel in range(0, 3)))
    
    RGBsToBin(rgbs, output)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-m", "--mode", choices=("frombin", "tobin"), default="frombin")
    parser.add_argument("-f", "--format", choices=("microsoft", "jasc"), default="jasc")
    parser.add_argument("-t", "--transparent", action='store_true')
    args = parser.parse_args()

    match args.mode:
        case "frombin":
            print(f"Converting {args.input} from binary to {args.format} .pal")
            if not args.output:
                args.output = os.path.splitext(args.input)[0] + ".pal"
            
            match args.format:
                case "jasc": # used by programs such as Aseprite
                    with open(args.input, "rb") as input, open(args.output, "w") as output:
                        binaryToJascPal(input, output, args.transparent)

                case "microsoft": # used by programs such as YY-CHR
                    with open(args.input, "rb") as input, open(args.output, "wb") as output:
                        binaryToMSPal(input, output, args.transparent)
                
        case "tobin":
            print(f"Converting {args.input} from .pal to binary")
            if not args.output:
                args.output = os.path.splitext(args.input)[0] + ".bin"
            
            match args.format:
                case "jasc":
                    with open(args.input, "r") as input, open(args.output, "wb") as output:
                        jascPalToBinary(input, output, args.transparent)
                    
                case "microsoft":
                    with open(args.input, "rb") as input, open(args.output, "wb") as output:
                        MSPalToBinary(input, output, args.transparent)