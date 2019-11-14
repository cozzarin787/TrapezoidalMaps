"""
    File: trapezoidal_map.py
    Authors: Jacob Cozzarin and William Carver

    Description: Trapezoidal map construction and planar point location implementation
"""
import matplotlib.pyplot as plt
import numpy as np
import sys

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

def main():
    set_figure_size([[0, 0], [100, 100]])
    construct_map_plot([[[5, 40], [55, 20]], [[30, 60], [70, 60]], [[60, 55], [95, 15]], [[40, 5], [95, 15]]])


if __name__ == "__main__":
    main()