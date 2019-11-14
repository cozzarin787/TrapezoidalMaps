"""
    File: trapezoidal_map.py
    Authors: Jacob Cozzarin and William Carver

    Description: Trapezoidal map construction and planar point location implementation
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

def cli_point_locate_prompt(trap_map):
    exit_commands = ["quit", "q", "exit", "e"]
    while True:
        # Parse input
        try:
            input_val = input("Enter a point (x y): ").strip()
            if input_val not in exit_commands:
                point = list(map(float, input_val.split(' ')))
                if len(point) != 2:
                    print("Error parsing point data, incorrect number of coordinates specified. Expected: x y")
                else:
                    result_path = locate_point(point, trap_map)
                    print(result_path)
            else:
                break;
        except Exception:
            print("Error parsing point data, make sure x and y coordinates are valid numbers")
        except KeyboardInterrupt:
            break;
    print("\nExiting point location prompt.")
    return

def construct_trapezoidal_map(lines, bound_box):
    # TODO
    # Data Structures:
        # Vertices need bullet info as well as the actual point data:
        # - Vertice of segment
        # - Top bullet path SEGMENT (vertice -> first intersection)
        # - Bottom bullet path SEGMENT (vertice -> first intersection)
        
        # Trapezoid is made up of:
        # - Top Segment
        # - Bottom Segment
        # - Bounding vertex on the left
        # - Bounding vertex on the right

        # X Internal Node (P NODE):
        # - Point p (endpoint of one line segment)
        # - Top bullet path SEGMENT (vertice -> segment above)
        # - Bottom bullet path SEGMENT (vertice -> segment below)
        # - Two children: 
        #   - Left: point that lies to the left of the vertical line passying through p
        #   - Right: point that lies to the right of the vertical line passying through p

        # Y Internal Node (S NODE):
        # - Line segment s
        # - Two children:
        #   - Left: anything ABOVE the line segment
        #   - Right: anything BELOW the line segment

    # ALGORITHM:
    # Insert new segment:
    # - Parse tree (point location with start point) until you get to a trapezoid (replaced with the start of the segment)
    #   - Case P NODE:
    #       - Check if point is to the left or right, take the appropriate child
    #   - Case Y NODE:
    #       - Check if point is above or below, take the appropriate child
    #   - Case Trapezoid:
    #       - Done, this is where we place the start point of the line segment
    # - Repeat above process for end point of segment
    return []

def locate_point(point, trap_map):
    # TODO
    return []

def set_figure_size(bounding_box):
    axes = plt.gca()
    axes.set_xlim([bounding_box[0][0], bounding_box[1][0]])
    axes.set_ylim([bounding_box[0][1], bounding_box[1][1]])

def make_line_and_bullets(p1, p2):
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')
    plt.axvline(x=p1[0], linestyle="--", color="tab:orange")
    plt.axvline(x=p2[0], linestyle="--", color="tab:orange")
    plt.plot(p1[0], p1[1], 'bo', markersize=3)
    plt.plot(p2[0], p2[1], 'bo', markersize=3)

def construct_map_plot(lines):
    for line in lines:
        make_line_and_bullets(line[0], line[1])
    try:
        plt.show()
    except:
        print("No display avaliable. Not displaying pyplot")

def print_usage():
    print("usage: python trapezoidal_map.py <fileName>")

def parseInput(filename):
    with open(filename) as f:
        num_lines = int(f.readline().rstrip())
        vals = [int(s) for s in str.split(f.readline().rstrip(), ' ')]
        bound_box = [[vals[0], vals[1]],[vals[2], vals[3]]]
        lines = []
        for line in f:
            if len(line) > 2:
                vals = [int(s) for s in str.split(line.rstrip(), " ")]
                lines.append( [[vals[0], vals[1]],[vals[2], vals[3]]] )

    return num_lines, bound_box, lines

def main():
    if len(sys.argv) == 2:
        num_lines, bound_box, lines = parseInput(sys.argv[1])
        set_figure_size(bound_box)
        trap_map = construct_trapezoidal_map(lines, bound_box)
        # Begin CLI
        cli_point_locate_prompt(trap_map)
        construct_map_plot(lines)
    else:
        print_usage()

if __name__ == "__main__":
    main()