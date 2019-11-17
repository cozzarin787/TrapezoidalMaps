"""
    File: trapezoidal_map.py
    Authors: Jacob Cozzarin and William Carver

    Description: Trapezoidal map construction and planar point location implementation
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

next_point = 0
next_segment = 0

class Trapezoid:
    def __init__(self, left_p, right_p, above_seg, below_seg, parent):
        self.left_point = left_p
        self.right_point = right_p
        self.above_segment = above_seg
        self.below_segment = below_seg
        self.parent = parent

    def isLeftBoundingTrap(self):
        if self.left_point == None:
            return True
        else:
            return False

    def isRightBoundingTrap(self):
        if self.right_point == None:
            return True
        else:
            return False

    def isTopBoundingTrap(self):
        if self.above_segment == None:
            return True
        else:
            return False

    def isBottomBoundingTrap(self):
        if self.below_segment == None:
            return True
        else:
            return False

class Segment:
    def __init__(self, left_point, right_point, parent, next_seg):
        self.parent = parent
        self.above = None
        self.below = None
        self.p = left_point
        self.q = right_point
        name = "S" + str(next_seg)
        self.m = (self.q.y - self.p.y) / (self.q.x - self.p.x)
        self.b = (self.p.y - (self.p.x * self.m))

    def getY(self, x):
        return self.m*x + self.b


class BeginPoint:
    bullet_upper = 100
    bullet_lower = 0

    def __init__(self, x, y, parent, next_pt):
        self.parent = parent
        self.left = None
        self.right = None
        self.loc = [x, y]
        name = "P" + str(next_pt)

class EndPoint:
    bullet_upper = 100
    bullet_lower = 0

    def __init__(self, x, y, parent, next_pt):
        self.parent = parent
        self.left = None
        self.right = None
        self.loc = [x, y]
        name = "Q" + str(next_pt)

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
    bb_top_p = BeginPoint(bound_box[0][0], bound_box[1][1], None, 0)
    bb_top_q = EndPoint(bound_box[1][0], bound_box[1][1], None, 0)
    bb_bot_p = BeginPoint(bound_box[0][0], bound_box[0][1], None, 0)
    bb_bot_q = EndPoint(bound_box[1][0], bound_box[0][1], None, 0)
    bb_top_s = Segment(bb_top_p, bb_top_q, None, 0)
    bb_bot_s = Segment(bb_bot_p, bb_bot_q, None, 0)
    trap_map = Trapezoid(bb_bot_p, bb_top_q, bb_top_s, bb_bot_s, None)

    for line in lines:
        print("Adding " + str(line))

        # Get trapezoids that contain P and Q
        t_p = locate_point(line[0], trap_map)
        t_q = locate_point(line[1], trap_map)

        next_point += 1 #update global counters
        next_segment += 1


        
        # CASE 2: Both endpoints are in the same trapezoid
        if t_p == t_q:
            # P will be Q's parent
            p = BeginPoint(line[0][0], line[0][1], t_p.parent, next_point)
            q = BeginPoint(line[1][0], line[1][1], p, next_point)
            s = Segment(p, q, None, next_segment)

            # Add trapezoid for P.left
            p.left = Trapezoid(t_p.left_point, p, t_p.above_segment, t_p.below_segment, p)

            # Add trapezoid for Q.right
            q.right = Trapezoid(q, t_q.right_point, t_p.above_segment, t_p.below_segment, q)

            # Add S as Q.left
            q.left = s

            # Add trapezoids for S left and right
            s.above = Trapezoid(p, q, t_p.above_segment, s, s)
            s.below = Trapezoid(p, q, s, t_p.below_segment, s)
            
            if t_p == None:
                # P is the new root
                trap_map = p
        else:
            # DO CASE 1 FOR BOTH ENDPOINTS
            # P and Q have different parents
            q = BeginPoint(line[1][0], line[1][1], t_q.parent, next_point)

            # Add segment for P.right

            # TEST FOR CASE 3

        # Update bullet paths for P and Q
        if t_p.isTopBoundingTrap():
            p.bullet_upper = bound_box[1][1]
        else:
            p.bullet_upper = t_p.above_segment.getY(p.loc[0])
        if t_q.isTopBoundingTrap():
            q.bullet_upper = bound_box[1][1]
        else:
            q.bullet_upper = t_q.above_segment.getY(q.loc[0])
        if t_p.isBottomBoundingTrap():
            p.bullet_lower = bound_box[0][1]
        else:
            p.bullet_lower = t_p.below_segment.getY(p.loc[0])
        if t_q.isBottomBoundingTrap():
            q.bullet_lower = bound_box[0][1]
        else:
            q.bullet_lower = t_q.below_segment.getY(q.loc[0])



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
    if trap_map == None:
        print("Error: Trap Map is None")
        return

    elif isinstance(trap_map, BeginPoint) or isinstance(trap_map, EndPoint):
        # Check to see if point is to the left or right of the given point
        if point[0] <= trap_map.loc[0]:
            locate_point(point, trap_map.left)
        else:
            locate_point(point, trap_map.right)

    elif isinstance(trap_map, Segment):
        # Check to see if point is above or below the given segment
        if point[1] >= trap_map.getY(point[0]):
            locate_point(point, trap_map.above)
        else:
            locate_point(point, trap_map.below)

    elif isinstance(trap_map, Trapezoid):
        return trap_map
    
    else:
        print("Error, unknown node type")

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
                if vals[0] < vals[2]:
                    lines.append( [[vals[0], vals[1]], [vals[2], vals[3]]] )
                else:
                    lines.append( [[vals[2], vals[3]], [vals[0], vals[1]]] )

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
