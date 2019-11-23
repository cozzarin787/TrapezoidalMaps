# TrapezoidalMaps
This program creates a trapezoidal map used for planar point location.

To run the program:

    python3 trapezoidal_map.py <input_file>

*NOTE*: Be sure to have matplotlib installed on your system, using pip

The program will create a trapezoidal map and a prompt will appear asking the user to enter a point "x y", the prompt will take the point, and output the appropriate traversal of the trapezoidal map. This prompt continues until "quit" or "q" is enter to the command line.

An adjacency matrix is created and written to a file named "output.txt"

Last, the program will try to output the visualization of the segments and bullet paths (trimmed). If no display is avaliable, a message will be displayed and exit the program.