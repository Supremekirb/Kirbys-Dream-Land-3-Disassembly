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


def binToRGBs(input: io.BufferedReader):
    rgbs: list[tuple[int, int, int]] = [[0, 0, 0]]
    while i:=input.read(2):
        assert len(i) == 2, "Input file is not a multiple of 2 bytes in size!"
        rgbs.append(fromBGR555(int.from_bytes(i, "little")))
    return rgbs

def binaryToJascPal(input: io.BufferedReader, output: io.TextIOWrapper):
    rgbs = binToRGBs(input)
    # this header stuff was copied from an example palette file /shrug
    output.write("JASC-PAL\n")
    output.write("0100\n")
    output.write("256\n")
    for i in range(0, 256):
        try:
            r, g, b = rgbs[i]
        except IndexError:
            r, g, b = 0, 0, 0

        output.write(str(r) + " ")
        output.write(str(g) + " ")
        output.write(str(b) + "\n")

def binaryToMSPal(input: io.BufferedReader, output: io.BufferedWriter):
    rgbs = binToRGBs(input)
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
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output", required=False)
    parser.add_argument("-m", "--mode", choices=("frombin", "tobin"), default="frombin")
    parser.add_argument("-f", "--format", choices=("microsoft", "jasc"), default="jasc")
    args = parser.parse_args()

    match args.mode:
        case "frombin":
            print(f"Converting {args.input} from binary to {args.format} .pal")
            if not args.output:
                args.output = os.path.splitext(args.input)[0] + ".pal"
                    
            match args.format:
                case "jasc": # used by programs such as Aseprite
                    with open(args.input, "wb") as input, open(args.output, "w") as output:
                        binaryToJascPal(input, output)

                case "microsoft": # used by programs such as YY-CHR
                    with open(args.input, "wb") as input, open(args.output, "wb") as output:
                        binaryToMSPal(input, output)
                
        case "tobin":
            print(f"Converting {args.input} from .pal to binary")
            if not args.output:
                args.output = os.path.splitext(args.input)[0] + ".bin"
            ...
            