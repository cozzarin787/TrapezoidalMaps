"""
    File: trapezoidal_map.py
    Authors: Jacob Cozzarin and William Carver

    Description: Trapezoidal map construction and planar point location implementation
"""
import sys

def parseInput(filename):
    print("Parsing!")
    with open(filename) as f:
        num_lines = int(f.readline().rstrip())
        vals = [int(s) for s in str.split(f.readline().rstrip(), ' ')]
        bound_box = [[vals[0], vals[1]],[vals[2], vals[3]]]
        lines = []
        for line in f:
            if len(line) > 2:
                vals = [int(s) for s in str.split(line.rstrip(), " ")]
                lines.append( [[vals[0], vals[1]],[vals[2], vals[3]]] )

    print(str(num_lines) + " in " + str(bound_box))
    print(lines)

    return num_lines, bound_box, lines

def main():
    print("Got to start somewhere, how about " + sys.argv[1])
    parseInput(sys.argv[1])

if __name__ == "__main__":
    main()