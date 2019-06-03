'''Classes for solving problems that can be modeled as a directed graph with goal nodes'''

# pylint: disable=too-few-public-methods, no-else-return
from collections import deque


class NodeSolver:
    '''Class for modeling problems that can be modeled as a directed graph with goal nodes'''
    def __init__(self, namer, detector, expander, follower):
        '''
        Whatever decides to use this gets to define what structure info is.
        namer: takes info representing a node and returns a hashable object (the name);
               names must be equal if and only if the nodes are equal
        detector: takes info and returns True if the node represented by the info is the goal node,
                  ...False otherwise.
        expander: takes info and returns an iterable of moves that can be made from the node
                  ...that the info represents. (a.k.a. paths leading out of that node)
        follower: takes info and a move that can be made from the node that the info represents,
                  ...and returns the info that represents the node that the move leads to
        '''
        self.get_name = namer
        self.is_goal = detector
        self.get_moves = expander
        self.follow_move = follower


class BFSSolver(NodeSolver):
    '''Class for solving node problems with breadth-first-search to reach the goal node'''
    def solve(self, start_info):
        '''
        Returns the list of moves needed to reach the goal node
        ...from the node represented by the parameter.
        Uses Breadth-first Search to go through the node tree
        '''
        if self.is_goal(start_info):
            return []

        start_name = self.get_name(start_info)

        # data is in the form (info, path)
        name_to_data = {start_name: (start_info, [])}
        queue = deque()

        queue.appendleft(start_name)

        while queue:
            current_name = queue.pop()
            current_info, current_path = name_to_data[current_name]

            expanded_moves = self.get_moves(current_info)
            # print("possible moves from {} is {}".format(current_info, expanded_moves))
            for move in expanded_moves:
                child_info = self.follow_move(current_info, move)
                child_path = current_path[:]
                child_path.append(move)

                if self.is_goal(child_info):
                    return child_path

                child_name = self.get_name(child_info)
                if child_name not in name_to_data:
                    # new, needs to be expanded
                    name_to_data[child_name] = (child_info, child_path)
                    queue.appendleft(child_name)
        return None
