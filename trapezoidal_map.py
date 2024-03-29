"""
    File: trapezoidal_map.py
    Authors: Jacob Cozzarin and William Carver

    Description: Trapezoidal map construction and planar point location implementation
"""

import matplotlib.pyplot as plt
import sys

class Trapezoid:
    """
    This is a class for representing a trapezoid for planar point location

    Attributes:
        left_point (BeginPoint or EndPoint): the left bounding vertex of the trapezoid
        right_point (BeginPoint or EndPoint): the right bounding vertex of the trapezoid
        above_segment (Segment): the upper bounding line of the trapezoid
        below_segment (Segment): the lower bounding line of the trapezoid
        parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
        name (string): name of the trapezoid
    """
    def __init__(self, left_p, right_p, above_seg, below_seg, parent):
        """
        The constructor for Trapezoid class

        Parameters:
            left_p (BeginPoint or EndPoint): the left bounding vertex of the trapezoid
            right_p (BeginPoint or EndPoint): the right bounding vertex of the trapezoid
            above_seg (Segment): the upper bounding line of the trapezoid
            below_seg (Segment): the lower bounding line of the trapezoid
            parent (BEginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
        """
        self.left_point = left_p
        self.right_point = right_p
        self.above_segment = above_seg
        self.below_segment = below_seg
        self.parent = parent

    def setName(self, name):
        """
        Set the name of the trapezoid

        Parameters:
            name (string): name to be assigned to the trapezoid
        """
        self.name = name

    def __str__(self):
        """
        ToString function for print the class for debug

        Returns:
            string: string representation of the Trapezoid class
        """
        return "(L:" + str(self.left_point) + \
               ", R:" + str(self.right_point) + \
               ", A:" + str(self.above_segment) + \
               ", B:" + str(self.below_segment) + ")"

    def __eq__(self, other):
        """
        Compares an object with this Trapezoid class to check for equality

        Parameters:
            other (any): object to check equality with this class

        Returns:
            Boolean: True if other is equal to this trapezoid, False otherwise
        """
        if isinstance(other, self.__class__):
            return self.left_point == other.left_point and \
                self.right_point == other.right_point and \
                self.above_segment == other.above_segment and \
                self.below_segment == other.below_segment
        else:
            return False

class Segment:
    """
    This is a class for representing a line segment for planar point location

    Attributes:
        parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
        above (BeginPoint, EndPoint, or Segment): planar point location object that is spatially above this segment
        below (BeginPoint, EndPoint, or Segment): planar point location object that is spatially below this segment
        p (BeginPoint): beginning point for this segment or left end point
        q (EndPoint): ending point for this segment or right end point
        name (string): name of the segment
        m (float): slope of the segment
        b (float): y-intercept of the segment
    """
    def __init__(self, left_point, right_point, parent, next_seg):
        """
        The constructor for Segment class

        Parameters:
            left_point (BeginPoint): beginning point for this segment or left end point
            right_point (EndPoint): ending point for this segment or right end point
            parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
            next_seg (int): number representing the id of the segment used for constructing the name
        """
        self.parent = parent
        self.above = None
        self.below = None
        self.p = left_point
        self.q = right_point
        self.name = "S" + str(next_seg)
        self.m = (self.q.loc[1] - self.p.loc[1]) / (self.q.loc[0] - self.p.loc[0])
        self.b = (self.p.loc[1] - (self.p.loc[0] * self.m))

    def __str__(self):
        """
        ToString method for the Segment class (name)

        Returns:
            string: name of the segment
        """
        return self.name

    def getY(self, x):
        """
        Calculates the y that lies on the segment given an x value

        Parameters:
            x (float): x value to calculate a give y value on the segment

        Returns:
            float: y coordinate at a given x value on the segment
        """
        return self.m*x + self.b

    def isAbove(self, other):
        """
        Given a planar point location object, check to see if it is above the segment

        Parameters: 
            other (BeginPoint, EndPoint, or Segment): planar point location object to check if it is above

        Returns:
            Boolean: True if other is above, else False
        """
        if isinstance(other, EndPoint) or isinstance(other, BeginPoint):
            return self.getY(other.loc[0]) > other.loc[1]
        elif isinstance(other, Segment):
            if self.getY(other.p.loc[0]) == other.p.loc[1]:
                # check other point
                return self.getY(other.q.loc[0]) > other.q.loc[1]
            return self.getY(other.p.loc[0]) > other.p.loc[1]
        else:   #Its a trap!
            return self.getY(other.above_segment.p.loc[0]) > other.above_segment.p.loc[1]
    
    def isOn(self, other):
        """
        Given a planar point location object, check to see if it lies on this segment

        Parameters: 
            other (BeginPoint, EndPoint, or Segment): planar point location object to check if it is on this segment

        Returns:
            Boolean: True if the other object lies on the segment, False otherwise
        """
        if isinstance(other, EndPoint) or isinstance(other, BeginPoint):
            return self.getY(other.loc[0]) == other.loc[1]
        elif isinstance(other, Segment):
            return self.getY(other.p.loc[0]) == other.p.loc[1]
        else:
            return self.getY(other.above_segment.p.loc[0]) == other.above_segment.p.loc[1]

    def __eq__(self, other):
        """
        Compares an object with this Segment class to check for equality

        Parameters:
            other (any): object to check equality with this class

        Returns:
            Boolean: True if other is equal to this segment, False otherwise
        """
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def replaceChild(self, oldChild, newChild):
        """
        Replaces oldChild with newChild

        Parameters:
            oldChild (BeginPoint, EndPoint, Segment, or Trapezoid): replaces this child with newChild
            newChild (BeginPoint, EndPoint, Segment, or Trapezoid): new child to replace oldChild with
        """
        if self.above == oldChild:
            self.above = newChild
        elif self.below == oldChild:
            self.below = newChild


class BeginPoint:
    """
    This is a class for representing a left end point of a segment for planar point location

    Attributes:
        parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
        left (BeginPoint, EndPoint, or Segment): planar point location object that is spatially to the left of this point
        right (BeginPoint, EndPoint, or Segment): planar point location object that is spatially to the right of this point
        loc (list): x and y coordinate of point
        name (string): name of the point
    """
    bullet_upper = 100
    bullet_lower = 0

    def __init__(self, x, y, parent, next_pt):
        """
        Constructor for the BeginPoint class

        Parameters:
            x (float): x coordinate of point
            y (float): y coordinate of point
            parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
            next_pt (int): number representing the id of the point used for constructing the name
        """
        self.parent = parent
        self.left = None
        self.right = None
        self.loc = [x, y]
        self.name = "P" + str(next_pt)
    
    def __str__(self):
        """
        ToString method for the BeginPoint class (name)

        Returns:
            string: name of the point
        """
        return self.name
    
    def replaceChild(self, oldChild, newChild):
        """
        Replaces oldChild with newChild

        Parameters:
            oldChild (BeginPoint, EndPoint, Segment, or Trapezoid): replaces this child with newChild
            newChild (BeginPoint, EndPoint, Segment, or Trapezoid): new child to replace oldChild with
        """
        if self.left == oldChild:
            self.left = newChild
        elif self.right == oldChild:
            self.right = newChild

class EndPoint:
    """
    This is a class for representing a right end point of a segment for planar point location

    Attributes:
        parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
        left (BeginPoint, EndPoint, or Segment): planar point location object that is spatially to the left of this point
        right (BeginPoint, EndPoint, or Segment): planar point location object that is spatially to the right of this point
        loc (list): x and y coordinate of point
        name (string): name of the point
    """
    bullet_upper = 100
    bullet_lower = 0

    def __init__(self, x, y, parent, next_pt):
        """
        Constructor for the EndPoint class

        Parameters:
            x (float): x coordinate of point
            y (float): y coordinate of point
            parent (BeginPoint, EndPoint, or Segment): parent pointer as part of the graph structure for traversal
            next_pt (int): number representing the id of the point used for constructing the name
        """
        self.parent = parent
        self.left = None
        self.right = None
        self.loc = [x, y]
        self.name = "Q" + str(next_pt)
    
    def __str__(self):
        """
        ToString method for the EndPoint class (name)

        Returns:
            string: name of the point
        """
        return self.name
    
    def replaceChild(self, oldChild, newChild):
        """
        Replaces oldChild with newChild

        Parameters:
            oldChild (BeginPoint, EndPoint, Segment, or Trapezoid): replaces this child with newChild
            newChild (BeginPoint, EndPoint, Segment, or Trapezoid): new child to replace oldChild with
        """
        if self.left == oldChild:
            self.left = newChild
        elif self.right == oldChild:
            self.right = newChild

def construct_trapezoidal_map(lines, bound_box):
    """
    This function constructs the acyclic graph representing the trapezoidal map. Given line segments
    and a bounding box, lines are inserted into the graph incrementally, creating the trapezoidal map after
    all line segments have been added to the map.

    Parameters:
        lines (list): list of segments represented as a left end point and right end point
        bound_box (list): list containing lower left and upper right point of the bounding box

    Returns:
        the root node of the acyclic graph representation of the trapezoidal map
    """
    duplicate_p = False
    duplicate_q = False # And let's hope they stay this way...

    next_point = 0
    next_segment = 0

    bb_top_p = BeginPoint(bound_box[0][0], bound_box[1][1], None, 0)
    bb_top_q = EndPoint(bound_box[1][0], bound_box[1][1], None, 0)
    bb_bot_p = BeginPoint(bound_box[0][0], bound_box[0][1], None, 0)
    bb_bot_q = EndPoint(bound_box[1][0], bound_box[0][1], None, 0)
    bb_top_s = Segment(bb_top_p, bb_top_q, None, 0)
    bb_bot_s = Segment(bb_bot_p, bb_bot_q, None, 0)
    the_tree = Trapezoid(bb_bot_p, bb_top_q, bb_top_s, bb_bot_s, None)

    for line in lines:
        #print("Adding " + str(line))
        #debugPrintTree(the_tree)
        #construct_map_plot(the_tree)
        
        # Get trapezoids that contain P and Q
        t_p = locate_point(line[0], the_tree)
        t_q = locate_point(line[1], the_tree)

        # Update global id counters
        next_point += 1 
        next_segment += 1

        # CASE 2: Both endpoints are in the same trapezoid
        if t_p == t_q:
            # P will be Q's parent
            p = BeginPoint(line[0][0], line[0][1], t_p.parent, next_point)
            q = EndPoint(line[1][0], line[1][1], p, next_point)
            s = Segment(p, q, q, next_segment)

            # Add trapezoid for P.left
            p.left = Trapezoid(t_p.left_point, p, t_p.above_segment, t_p.below_segment, p)

            # Add trapezoid for Q.right
            q.right = Trapezoid(q, t_q.right_point, t_p.above_segment, t_p.below_segment, q)

            # Add S as Q.left
            q.left = s

            # Add q to the right of p
            p.right = q

            # Add trapezoids for S left and right
            s.above = Trapezoid(p, q, t_p.above_segment, s, s)
            s.below = Trapezoid(p, q, s, t_p.below_segment, s)

            if t_p.parent is None:
                # P is the new root
                the_tree = p
            else:
                # t_p's parent should abandon t_p and adopt p in its place...
                t_p.parent.replaceChild(t_p, p)
        else:
            duplicate_p = False
            duplicate_q = False
            # CASE 1 FOR BOTH ENDPOINTS since P and Q have different parents
            if isinstance(t_p, BeginPoint) or isinstance(t_p, EndPoint):
                # P is a duplicate point
                duplicate_p = True
                #print("P is a duplicate point!")    # Wow, P sure is special
                p = t_p
            else:
                # Normal handling of P
                p = BeginPoint(line[0][0], line[0][1], t_p.parent, next_point)
                t_p.parent.replaceChild(t_p, p)


            if isinstance(t_q, BeginPoint) or isinstance(t_q, EndPoint):
                # Q is a duplicate point...
                duplicate_q = True
                #print("Q is a duplicate point!")    # Tell the world how special Q is
                q = t_q
            else:
                # Normal handling of Q
                q = EndPoint(line[1][0], line[1][1], t_q.parent, next_point)
                t_q.parent.replaceChild(t_q, q)
                
            if not duplicate_p:
                # Normal handling of P
                # Add segment for P.right
                s = Segment(p, q, p, next_segment)
                p.right = s

                # Add Trapezoid for P.left
                p.left = Trapezoid(t_p.left_point, p, t_p.above_segment, t_p.below_segment, p)

                # Add Trapezoids for S.above and S.below
                if isinstance(t_p.parent, BeginPoint) and t_p.parent.loc[1] >= s.getY(t_p.parent.loc[0]):
                    s.above = Trapezoid(p, t_p.right_point, t_p.above_segment, s, s)
                    t_p.right_point.bullet_lower = s.getY(t_p.right_point.loc[0])
                    s.below = Trapezoid(p, findRightPointBelow(the_tree, s), s, t_p.below_segment, s)

                elif isinstance(t_p.parent, BeginPoint) and t_p.parent.loc[1] < s.getY(t_p.parent.loc[0]):
                    s.above = Trapezoid(p, findRightPointAbove(the_tree, s), t_p.above_segment, s, s)
                    s.below = Trapezoid(p, t_p.right_point, s, t_p.below_segment, s)
                    t_p.right_point.bullet_upper = s.getY(t_p.right_point.loc[0])

                elif isinstance(t_p.parent, Segment) and p.loc[1] >= t_p.parent.getY(p.loc[0]):
                    s.above = Trapezoid(p, findRightPointAbove(the_tree, s), t_p.above_segment, s, s)
                    s.below = Trapezoid(p, t_p.right_point, s, t_p.below_segment, s)
                    t_p.right_point.bullet_upper = s.getY(t_p.right_point.loc[0])

                elif isinstance(t_p.parent, Segment) and p.loc[1] < t_p.parent.getY(p.loc[0]):
                    s.above = Trapezoid(p, t_p.right_point, t_p.above_segment, s, s)
                    t_p.right_point.bullet_lower = s.getY(t_p.right_point.loc[0])
                    s.below = Trapezoid(p, findRightPointBelow(the_tree, s), s, t_p.below_segment, s)


            if not duplicate_q:
                # Normal handling of Q's segment
                # Add segment for Q.left
                s = Segment(p, q, q, next_segment)
                q.left = s

                # Add Trapezoid for Q.right
                q.right = Trapezoid(q, t_q.right_point, t_q.above_segment, t_q.below_segment, q)

                # Add Trapezoids for S.above and S.below
                if isinstance(t_q.parent, EndPoint) and t_q.parent.loc[1] >= s.getY(t_q.parent.loc[0]):
                    s.above = Trapezoid(t_q.left_point, q, t_q.above_segment, s, s)
                    t_q.left_point.bullet_lower = s.getY(t_q.left_point.loc[0])
                    s.below = Trapezoid(findLeftPointBelow(the_tree, s), q, s, t_q.below_segment, s)

                elif isinstance(t_q.parent, EndPoint) and t_q.parent.loc[1] < s.getY(t_q.parent.loc[0]):
                    s.above = Trapezoid(findLeftPointAbove(the_tree, s), q, t_q.above_segment, s, s)
                    s.below = Trapezoid(t_q.left_point, q, s, t_q.below_segment, s)
                    t_q.left_point.bullet_upper = s.getY(t_q.left_point.loc[0])

                elif isinstance(t_q.parent, Segment) and p.loc[1] >= t_q.parent.getY(p.loc[0]):
                    s.above = Trapezoid(findLeftPointAbove(the_tree, s), q, t_q.above_segment, s, s)
                    s.below = Trapezoid(t_q.left_point, q, s, t_q.below_segment, s)
                    t_q.left_point.bullet_upper = s.getY(t_q.left_point.loc[0])

                elif isinstance(t_q.parent, Segment) and p.loc[1] < t_q.parent.getY(p.loc[0]):
                    s.above = Trapezoid(t_q.left_point, q, t_q.above_segment, s, s)
                    s.below = Trapezoid(findLeftPointBelow(the_tree, s), q, s, t_q.below_segment, s)
                    t_q.left_point.bullet_lower = s.getY(t_q.left_point.loc[0])

            # CASE 3   :(
            high_trap = Trapezoid(p, q, bb_top_s, Segment(p, q, None, next_segment), None)
            low_trap = Trapezoid(p, q, Segment(p, q, None, next_segment), bb_bot_s, None)
            blockBullets(the_tree, p, q, high_trap, low_trap, next_segment, duplicate_p, duplicate_q)
            

        # Update bullet paths for P and Q
        if not duplicate_p:
            p.bullet_upper = t_p.above_segment.getY(p.loc[0])
            p.bullet_lower = t_p.below_segment.getY(p.loc[0])
        if not duplicate_q:
            q.bullet_upper = t_q.above_segment.getY(q.loc[0])
            q.bullet_lower = t_q.below_segment.getY(q.loc[0])

    #print("ALL DONE(?)")
    #debugPrintTree(the_tree)
    #construct_map_plot(the_tree)
    return the_tree

def debugPrintTree(tree, offset = ""):
    """
    Debug function for printing out a given trapezoidal map
    """
    if tree is None:
        print(offset + "D'OH!")
    else:
        print(offset + str(tree))
        if len(offset) % 2 == 0:
            offset = offset + "|"
        else:
            offset = offset + " "
    if isinstance(tree, BeginPoint) or isinstance(tree, EndPoint):
        print(offset + "left:")
        debugPrintTree(tree.left, offset)
        print(offset + "right:")
        debugPrintTree(tree.right, offset)
    if isinstance(tree, Segment):
        print(offset + "above:")
        debugPrintTree(tree.above, offset)
        print(offset + "below:")
        debugPrintTree(tree.below, offset)

def blockBullets(tree, left_point, right_point, high_trap, low_trap, seg_name, handleLeftDupes = False, handleRightDupes = False):
    """

    """
    #print("blocking at " + str(tree))
    if isinstance(tree, Trapezoid):
        s = Segment(left_point, right_point, tree.parent, seg_name)
        # Determine sides of new trapezoids, trimming bullet paths accordingly
        if s.isAbove(tree.left_point):
            above_left = high_trap.left_point
            below_left = tree.left_point
            if not s.isOn(tree.left_point):
                tree.left_point.bullet_upper = s.getY(tree.left_point.loc[0])
        else:
            above_left = tree.left_point
            below_left = low_trap.left_point
            if not s.isOn(tree.left_point):
                tree.left_point.bullet_lower = s.getY(tree.left_point.loc[0])

        if s.isAbove(tree.right_point):
            above_right = high_trap.right_point
            below_right = tree.right_point
            if not s.isOn(tree.right_point):
                tree.right_point.bullet_upper = s.getY(tree.right_point.loc[0])
        else:
            above_right = tree.right_point
            below_right = low_trap.right_point
            if not s.isOn(tree.right_point):
                tree.right_point.bullet_lower = s.getY(tree.right_point.loc[0])

        # Make the new trapezoids
        s.above = Trapezoid(above_left, above_right, high_trap.above_segment, s, s)
        s.below = Trapezoid(below_left, below_right, s, low_trap.below_segment, s)

        # Gotta insert the new segment
        tree.parent.replaceChild(tree, s)

    elif isinstance(tree, Segment):
        # if new segment is above
        if tree.isAbove(left_point):
            # Shrink high_trap
            short_high_trap = Trapezoid(rightMostPoint(high_trap.left_point, tree.p), leftMostPoint(high_trap.right_point, tree.q), tree, high_trap.below_segment, None)
            blockBullets(tree.below, left_point, right_point, short_high_trap, low_trap, seg_name, handleLeftDupes, handleRightDupes)
        else:
            # Shrink low_trap
            short_low_trap = Trapezoid(rightMostPoint(low_trap.left_point, tree.p), leftMostPoint(low_trap.right_point, tree.q), low_trap.above_segment, tree, None)
            blockBullets(tree.above, left_point, right_point, high_trap, short_low_trap, seg_name, handleLeftDupes, handleRightDupes)

    else: # tree is a point
        if (handleLeftDupes == False and tree == left_point) or (handleRightDupes == False and tree == right_point):
            return # Don't bother going deeper when we hit our own endpoints
        if tree.loc[0] <= left_point.loc[0]:
            # Just traverse right
            blockBullets(tree.right, left_point, right_point, high_trap, low_trap, seg_name, handleLeftDupes, handleRightDupes)
        elif tree.loc[0] >= right_point.loc[0]:
            # Just traverse left
            blockBullets(tree.left, left_point, right_point, high_trap, low_trap, seg_name, handleLeftDupes, handleRightDupes)
        else:
            # Split the recursion, traverse both directions, and update bullet paths
            s = Segment(left_point, right_point, None, "_")    # For calculations, not actually saved in the tree
            if s.isAbove(tree):
                # Split lower trapezoid and traverse both directions
                low_trap_left = Trapezoid(low_trap.left_point, tree, s, low_trap.below_segment, s)
                low_trap_right = Trapezoid(tree, low_trap.right_point, s, low_trap.below_segment, s)
                blockBullets(tree.left, left_point, right_point, high_trap, low_trap_left, seg_name, handleLeftDupes, handleRightDupes)
                blockBullets(tree.right, left_point, right_point, high_trap, low_trap_right, seg_name, handleLeftDupes, handleRightDupes)
            else:
                # Split higher trapezoid and traverse both directions
                high_trap_left = Trapezoid(high_trap.left_point, tree, high_trap.above_segment, s, s)
                high_trap_right = Trapezoid(tree, high_trap.right_point, high_trap.above_segment, s, s)
                blockBullets(tree.left, left_point, right_point, high_trap_left, low_trap, seg_name, handleLeftDupes, handleRightDupes)
                blockBullets(tree.right, left_point, right_point, high_trap_right, low_trap, seg_name, handleLeftDupes, handleRightDupes)
        

def findLeftPointAbove(cur, seg):    
    """
    When constructing a trapezoid, this function figures out the left bound vertex relative to
    the trapezoid above the segment we are looking at
    """
    # ANY POINT IS FAIR GAME
    if isinstance(cur, BeginPoint) or isinstance(cur, EndPoint):
        # if cur.x > q.x
        if cur.loc[0] > seg.q.loc[0]:
            # Just look left
            return findLeftPointAbove(cur.left, seg)
        elif cur == seg.q:
            return None
        elif cur == seg.p:
            return seg.p
        else:
            r = findLeftPointAbove(cur.right, seg)
            l = findLeftPointAbove(cur.left, seg)
            if not seg.isAbove(cur): # if cur is above seg include it
                return rightMostPoint(l, r, cur)
            else:   # otherwise just check l and r
                return rightMostPoint(l, r)
    elif isinstance(cur, Segment):
        if cur.isAbove(seg):
            return findLeftPointAbove(cur.below, seg)
        else:
            return findLeftPointAbove(cur.above, seg)
    else:
        # It's a trap!
        return None


def findLeftPointBelow(cur, seg):    
    """
    When constructing a trapezoid, this function figures out the left bound vertex relative to
    the trapezoid below the segment we are looking at
    """
    # ANY POINT IS FAIR GAME
    if isinstance(cur, BeginPoint) or isinstance(cur, EndPoint):
        # if cur.x > q.x
        if cur.loc[0] > seg.q.loc[0]:
            # Just look left
            return findLeftPointBelow(cur.left, seg)
        elif cur == seg.q:
            return None
        elif cur == seg.p:
            return seg.p
        else:
            r = findLeftPointBelow(cur.right, seg)
            l = findLeftPointBelow(cur.left, seg)
            if seg.isAbove(cur): # if cur is below seg include it
                return rightMostPoint(l, r, cur)
            else:   # otherwise just check l and r
                return rightMostPoint(l, r)
    elif isinstance(cur, Segment):
        if cur.isAbove(seg):
            return findLeftPointBelow(cur.below, seg)
        else:
            return findLeftPointBelow(cur.above, seg)
    else:
        # cur is a trapezoid, ignore it
        return None


def rightMostPoint(left, right, cur = None):
    """
    compares two points and checks to see which point is the closest to cur, but is to the right as well
    """
    bestPoint = left
    if (bestPoint is None) or ((not right is None) and (bestPoint.loc[0] < right.loc[0])):
        bestPoint = right
    if (bestPoint is None) or ((not cur is None) and (bestPoint.loc[0] < cur.loc[0])):
        bestPoint = cur
    return bestPoint


def findRightPointAbove(cur, seg):   
    """
    When constructing a trapezoid, this function figures out the right bound vertex relative to
    the trapezoid above the segment we are looking at
    """ 
    # ANY POINT IS FAIR GAME
    if isinstance(cur, BeginPoint) or isinstance(cur, EndPoint):
        # if cur.x < p.x
        if cur.loc[0] < seg.p.loc[0]:
            # Just look right
            return findRightPointAbove(cur.right, seg)
        elif cur == seg.q:
            return seg.q
        elif cur == seg.p:
            return None
        else:
            r = findRightPointAbove(cur.right, seg)
            l = findRightPointAbove(cur.left, seg)
            if not seg.isAbove(cur): # if cur is above seg include it
                return leftMostPoint(l, r, cur)
            else:   # otherwise just check l and r
                return leftMostPoint(l, r)
    elif isinstance(cur, Segment):
        if cur.isAbove(seg):
            return findRightPointAbove(cur.below, seg)
        else:
            return findRightPointAbove(cur.above, seg)
    else:
        # It's a trap!
        return None


def findRightPointBelow(cur, seg):  
    """
    When constructing a trapezoid, this function figures out the right bound vertex relative to
    the trapezoid below the segment we are looking at
    """  
    # ANY POINT IS FAIR GAME
    if isinstance(cur, BeginPoint) or isinstance(cur, EndPoint):
        # if cur.x < p.x
        if cur.loc[0] < seg.p.loc[0]:
            return findRightPointBelow(cur.right, seg)
        elif cur == seg.q:
            return seg.q
        elif cur == seg.p:
            return None
        else:
            r = findRightPointBelow(cur.right, seg)
            l = findRightPointBelow(cur.left, seg)
            if seg.isAbove(cur): # if cur is below seg include it
                return leftMostPoint(l, r, cur)
            else:   # otherwise just check l and r
                return leftMostPoint(l, r)
    elif isinstance(cur, Segment):
        if cur.isAbove(seg):
            return findRightPointBelow(cur.below, seg)
        else:
            return findRightPointBelow(cur.above, seg)
    else:
        # cur is a trapezoid, ignore it
        return None


def leftMostPoint(left, right, cur = None):
    """
    compares two points and checks to see which point is the closest to cur, but is to the left as well
    """
    bestPoint = left
    # if bp is none OR 
    if (bestPoint is None) or ((not right is None) and (bestPoint.loc[0] > right.loc[0])):
        bestPoint = right
    if (bestPoint is None) or ((not cur is None) and (bestPoint.loc[0] > cur.loc[0])):
        bestPoint = cur
    return bestPoint

def name_and_count_traps(trap_map, trap_set, cur_b_count, cur_e_count, cur_t_count):
    """
    This function counts the number of BeginPoints, EndPoints (duplicate points will lower the count), and Trapezoids. 
    As well as, naming each unique trapezoid
    """
    if isinstance(trap_map, BeginPoint):
        left_b_count, left_e_count, cur_t_count = name_and_count_traps(trap_map.left, trap_set, cur_b_count, cur_e_count, cur_t_count)
        right_b_count, right_e_count, right_t_count = name_and_count_traps(trap_map.right, trap_set, cur_b_count, cur_e_count, cur_t_count)
        return (left_b_count + right_b_count + 1, left_e_count + right_e_count, right_t_count)
    elif isinstance(trap_map, EndPoint):
        left_b_count, left_e_count, cur_t_count = name_and_count_traps(trap_map.left, trap_set, cur_b_count, cur_e_count, cur_t_count)
        right_b_count, right_e_count, right_t_count = name_and_count_traps(trap_map.right, trap_set, cur_b_count, cur_e_count, cur_t_count)
        return (left_b_count + right_b_count, left_e_count + right_e_count + 1, right_t_count)
    elif isinstance(trap_map, Segment):
        left_b_count, left_e_count, cur_t_count = name_and_count_traps(trap_map.above, trap_set, cur_b_count, cur_e_count, cur_t_count)
        right_b_count, right_e_count, right_t_count = name_and_count_traps(trap_map.below, trap_set, cur_b_count, cur_e_count, cur_t_count)
        return (left_b_count + right_b_count, left_e_count + right_e_count, right_t_count)
    else:
        if trap_map in trap_set:
            trap_map.setName(trap_set[trap_set.index(trap_map)].name)
            return (cur_b_count, cur_e_count, cur_t_count)
        else:
            trap_map.setName("T"+str(cur_t_count+1))
            trap_set.append(trap_map)
            return (cur_b_count, cur_e_count, cur_t_count + 1)

def populate_adjacency_matrix(trap_map, matrix, num_begin_points, num_end_points, num_lines):
    """
    This function converts a trapezoidal map (acyclic graph) into an adjacency matrix.
    """
    # Children adjacency addition
    base_index = -1
    left_index = -1
    right_index = -1
    above_index = -1
    below_index = -1
    if isinstance(trap_map, BeginPoint):
        # Get Base index of current node
        base_index = int(trap_map.name[1:]) - 1
        # Get Left Child Index
        if isinstance(trap_map.left, BeginPoint):
            left_index = int(trap_map.left.name[1:]) - 1
        elif isinstance(trap_map.left, EndPoint):
            left_index = int(trap_map.left.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.left, Segment):
            left_index = int(trap_map.left.name[1:]) + num_begin_points + num_end_points - 1
        else:
            left_index = int(trap_map.left.name[1:]) + num_begin_points + num_end_points + num_lines - 1
        # Get Right Child Index
        if isinstance(trap_map.right, BeginPoint):
            right_index = int(trap_map.right.name[1:]) - 1
        elif isinstance(trap_map.right, EndPoint):
            right_index = int(trap_map.right.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.right, Segment):
            right_index = int(trap_map.right.name[1:]) + num_begin_points + num_end_points - 1
        else:
            right_index = int(trap_map.right.name[1:]) + num_begin_points + num_end_points + num_lines - 1

        # Update Adjacency Matrix
        matrix[left_index][base_index] = 1
        matrix[right_index][base_index] = 1

        # Traverse down to the children
        populate_adjacency_matrix(trap_map.left, matrix, num_begin_points, num_end_points, num_lines)
        populate_adjacency_matrix(trap_map.right, matrix, num_begin_points, num_end_points, num_lines)
    elif isinstance(trap_map, EndPoint):
        # Get Base index of current node
        base_index = int(trap_map.name[1:]) + num_begin_points - 1
        # Get Left Child Index
        if isinstance(trap_map.left, BeginPoint):
            left_index = int(trap_map.left.name[1:]) - 1
        elif isinstance(trap_map.left, EndPoint):
            left_index = int(trap_map.left.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.left, Segment):
            left_index = int(trap_map.left.name[1:]) + num_begin_points + num_end_points - 1
        else:
            left_index = int(trap_map.left.name[1:]) + num_begin_points + num_end_points + num_lines - 1
        # Get Right Child Index
        if isinstance(trap_map.right, BeginPoint):
            right_index = int(trap_map.right.name[1:]) - 1
        elif isinstance(trap_map.right, EndPoint):
            right_index = int(trap_map.right.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.right, Segment):
            right_index = int(trap_map.right.name[1:]) + num_begin_points + num_end_points - 1
        else:
            right_index = int(trap_map.right.name[1:]) + num_begin_points + num_end_points + num_lines - 1

        # Update Adjacency Matrix
        matrix[left_index][base_index] = 1
        matrix[right_index][base_index] = 1
        # Traverse down to the children
        populate_adjacency_matrix(trap_map.left, matrix, num_begin_points, num_end_points, num_lines)
        populate_adjacency_matrix(trap_map.right, matrix, num_begin_points, num_end_points, num_lines)
    elif isinstance(trap_map, Segment):
        # Get Base index of current node
        base_index = int(trap_map.name[1:]) + num_begin_points + num_end_points - 1
        # Get Above Child Index
        if isinstance(trap_map.above, BeginPoint):
            above_index = int(trap_map.above.name[1:]) - 1
        elif isinstance(trap_map.above, EndPoint):
            above_index = int(trap_map.above.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.above, Segment):
            above_index = int(trap_map.above.name[1:]) + num_begin_points + num_end_points - 1
        else:
            above_index = int(trap_map.above.name[1:]) + num_begin_points + num_end_points + num_lines - 1
        # Get Below Child Index
        if isinstance(trap_map.below, BeginPoint):
            below_index = int(trap_map.below.name[1:]) - 1
        elif isinstance(trap_map.below, EndPoint):
            below_index = int(trap_map.below.name[1:]) + num_begin_points - 1
        elif isinstance(trap_map.below, Segment):
            below_index = int(trap_map.below.name[1:]) + num_begin_points + num_end_points - 1
        else:
            below_index = int(trap_map.below.name[1:]) + num_begin_points + num_end_points + num_lines - 1
        
        # Update Adjacency Matrix
        matrix[above_index][base_index] = 1
        matrix[below_index][base_index] = 1

        # Traverse down to the children
        populate_adjacency_matrix(trap_map.above, matrix, num_begin_points, num_end_points, num_lines)
        populate_adjacency_matrix(trap_map.below, matrix, num_begin_points, num_end_points, num_lines)
    
def create_adjacency_matrix(trap_map, num_lines):
    """
    Calls a number of helper functions to name trapezoids, construct an adjacency matrix, and then write the
    matrix contents to a file.
    """
    # Parse trap map to get total num of trapezoids
    num_begin_points, num_end_points, num_traps = name_and_count_traps(trap_map, [], 0, 0, 0)
    matrix_dim = num_begin_points + num_end_points + num_traps + num_lines
    matrix = [[0 for x in range(matrix_dim)] for y in range(matrix_dim)] 
    # Populate matrix with adjacency values
    populate_adjacency_matrix(trap_map, matrix, num_begin_points, num_end_points, num_lines)
    # print matrix to file
    fp = open("output.txt", "w")
    row_sum = 0
    col_sum = 0
    col_sums = []
    row_str = ""
    for i in range(0, matrix_dim):
        row_sum = 0
        col_sum = 0
        row_str = ""
        for j in range(0, matrix_dim):
            row_sum += int(matrix[i][j])
            row_str += str(matrix[i][j]) + " "
        for j in range(0, matrix_dim):
            col_sum += int(matrix[j][i])
        col_sums.append(col_sum)
        row_str += str(row_sum)
        print(row_str, file=fp)
    row_str = ""
    for i in range(0, matrix_dim):
        row_str += str(col_sums[i]) + " "
    print(row_str, file=fp)

    fp.close()
    
def cli_point_locate_prompt(trap_map):
    """
    This function creates the command line interface where the user can enter a point. The path taken
    in the acyclic graph representation of the trapezoidal map is returned to the user.
    """
    exit_commands = ["quit", "q", "exit", "e"]
    while True:
        # Parse input
        try:
            input_val = input("Enter a point (x y) Type quit to exit: ").strip()
            if input_val not in exit_commands:
                point = list(map(float, input_val.split(' ')))
                if len(point) != 2:
                    print("Error parsing point data, incorrect number of coordinates specified. Expected: x y")
                else:
                    result_path = []
                    result_str = ""
                    trap = locate_point(point, trap_map)
                    result_path.append(trap.name)
                    while trap.parent != None:
                        trap = trap.parent
                        result_path.append(trap.name)
                    result_path.reverse()
                    for node in result_path:
                        result_str += node + " "
                    print(result_str)
            else:
                break
        except Exception:
            print("Error parsing point data, make sure x and y coordinates are valid numbers")
        except KeyboardInterrupt:
            break
    print("\nExiting point location prompt.")
    return

def locate_point(point, trap_map):
    """
    Given a point, this function traverses the trapezoidal map, finding the trapezoid the point is in
    """
    if trap_map == None:
        print("Error: Trap Map is None")
        return

    elif isinstance(trap_map, BeginPoint) or isinstance(trap_map, EndPoint):
        # Check to see if point is to the left or right of the given point
        if point[0] == trap_map.loc[0]:
            if point[1] == trap_map.loc[1]:
                # A duplicate point? Return that bad boy!
                return trap_map
            else:
                return locate_point(point, trap_map.left)
        elif point[0] < trap_map.loc[0]:
            return locate_point(point, trap_map.left)
        else:
            return locate_point(point, trap_map.right)

    elif isinstance(trap_map, Segment):
        # Check to see if point is above or below the given segment
        if point[1] >= trap_map.getY(point[0]):
            return locate_point(point, trap_map.above)
        else:
            return locate_point(point, trap_map.below)

    elif isinstance(trap_map, Trapezoid):
        return trap_map
    
    else:
        print("Error, unknown node type")

def set_figure_size(bounding_box):
    """
    Sets the size of the plot displayed to the bounding box of the trapezoidal map
    """
    axes = plt.gca()
    axes.set_xlim([bounding_box[0][0], bounding_box[1][0]])
    axes.set_ylim([bounding_box[0][1], bounding_box[1][1]])

def add_line_to_plot(line):
    """
    Adds a line to the plot
    """
    plt.plot([line.p.loc[0], line.q.loc[0]], [line.p.loc[1], line.q.loc[1]], 'b-')

def add_point_and_bullets_to_plot(point):
    """
    Adds a point and its corresponding trimmed bullet paths to the plot
    """
    # point
    plt.plot(point.loc[0], point.loc[1], 'bo', markersize=3)
     # upper bullet
    plt.plot([point.loc[0], point.loc[0]], [point.loc[1], point.bullet_upper], linestyle="--", color="tab:orange")
    # lower bullet
    plt.plot([point.loc[0], point.loc[0]], [point.loc[1], point.bullet_lower], linestyle="--", color="tab:orange")

def create_plot_from_trap_map(trap_map, line_set):
    """
    Creates a displayed plot of the entire trapezoidal map
    """
    if isinstance(trap_map, BeginPoint) or isinstance(trap_map, EndPoint):
        # Add point to plot
        add_point_and_bullets_to_plot(trap_map)
        create_plot_from_trap_map(trap_map.left, line_set)
        create_plot_from_trap_map(trap_map.right, line_set)
    elif isinstance(trap_map, Segment):
        # Add segment to plot/line_set, check to see if segment already added
        if trap_map not in line_set:
            add_line_to_plot(trap_map)
            line_set.append(trap_map)
        create_plot_from_trap_map(trap_map.above, line_set)
        create_plot_from_trap_map(trap_map.below, line_set)

def construct_map_plot(trap_map, bound_box):
    """
    Calls helper function to construct the plot of the trapezoidal map, and tries to display.
    Message shown if display is not avaliable.
    """
    try:
        set_figure_size(bound_box)
        create_plot_from_trap_map(trap_map, [])
        plt.show()
    except:
        print("No display avaliable. Not displaying pyplot")

def print_usage():
    """
    Prints usage for the program
    """
    print("usage: python trapezoidal_map.py <fileName>")

def parseInput(filename):
    """
    Pase input file containing number of segments, bounding box dimensions, and segment information
    """
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
    """
    Entry point of the program, calling all of the higher level functions to 
        - Create trapezoidal map
        - Create adjacency matrix representation
        - Create command line interface for user to do planar point location
        - Create plot of trapezoidal map and display to user
    """
    if len(sys.argv) == 2:
        num_lines, bound_box, lines = parseInput(sys.argv[1])
        trap_map = construct_trapezoidal_map(lines, bound_box)
        create_adjacency_matrix(trap_map, num_lines)
        # Begin CLI
        cli_point_locate_prompt(trap_map)
        construct_map_plot(trap_map, bound_box)
    else:
        print_usage()

if __name__ == "__main__":
    main()
