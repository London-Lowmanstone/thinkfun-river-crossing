'''
Framework for modeling the game River Crossing

See terms.txt for the types of the different terms.
'''

# pylint: disable=too-few-public-methods, no-else-return, too-many-arguments

WIDTH = 5
HEIGHT = 7
UP, RIGHT, DOWN, LEFT = [0, 1, 2, 3]

class Board:
    '''
    Represents a River Crossing board
    '''
    def __init__(self, start, finish, pegs, planks, held_plank=None):
        # the starting position of the person
        # form: peg
        self.person_position = start
        # the finish position for the person
        self.finish = finish
        # the pegs on the board
        # form: set of pegs
        self.pegs = set()
        self.add_pegs(pegs)
        # the planks on the board
        # form: set of planks
        self.planks = set()
        # pegs that are covered by planks
        # form: set of pegs
        self._covered_points = set()
        self.add_planks(planks)
        # if the person is carrying a plank
        # form: held plank
        self.held_plank = held_plank

    def __str__(self):
        return "<Board: person position: {}, pegs: {}, planks: {}, held_plank: {}>".format(self.person_position, self.pegs, self.planks, self.held_plank) # pylint: disable=line-too-long

    def __eq__(self, other):
        if isinstance(other, Board):
            for attribute in ['person_position', 'finish', 'pegs', 'planks', 'held_plank']:
                if getattr(self, attribute) != getattr(other, attribute):
                    return False
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.person_position) + hash(tuple(self.planks))

    def __deepcopy__(self, memo):
        # ignoring `memo` as per https://stackoverflow.com/a/1950593/
        return Board(self.person_position, self.finish, self.pegs.copy(),
                     self.planks.copy(), self.held_plank)

    def get_moves(self):
        '''Returns a list of all of the available moves'''
        moves = []
        walk_moves = self.get_walk_moves()

        if self.can_grab_plank():
            plank_moves = [("grab", plank_peg) for plank_peg in self.get_grab_planks()]
        else:
            plank_moves = [("place", plank_peg) for plank_peg in self.get_place_planks()]

        moves.extend(walk_moves)
        moves.extend(plank_moves)
        return moves

    def get_walk_moves(self):
        '''Returns a list of all of the available walk moves'''
        ans = []
        for plank in self.planks:
            index = None
            for possible_index in range(2):
                if plank[possible_index] == self.person_position:
                    index = possible_index

            if index is not None:
                index = (index + 1) % 2 # we want the other peg
                peg = plank[index]
                ans.append(("walk", peg))

        return ans

    def get_grab_planks(self):
        '''
        Returns a list of all of the available grab moves.
        Assumption: there is no held plank.
        '''
        # upgrade: this is computed twice, which is inefficient
        # any place you can walk to is also a place where you can grab a plank
        return [move for move_type, move in self.get_walk_moves()]

    def get_place_planks(self):
        '''
        Returns a list of all of the available place moves.
        Assumption: there is a held plank.
        '''
        ans = []
        for direction in range(4):
            peg = get_peg_in_direction(self.person_position, direction, self.held_plank)
            if peg is not None and peg in self.pegs:
                works = True
                for waypoint in get_waypoints((self.person_position, peg)):
                    if waypoint in self._covered_points or waypoint in self.pegs:
                        works = False
                        break
                if works:
                    ans.append(peg)
        return ans

    def make_move(self, move):
        '''Makes a move'''
        move_type, move = move
        if move_type == "walk":
            self.person_position = move
        elif move_type == "grab":
            self.held_plank = get_peg_dist(self.person_position, move)
            self.remove_plank(get_plank(self.person_position, move))
        elif move_type == "place":
            self.add_plank(get_plank(self.person_position, move))
            self.held_plank = None
        else:
            raise ValueError("Move type {} not recognized".format(move_type))

    def solved(self):
        '''Returns boolean whether or not the game has been solved'''
        return self.person_position == self.finish

    def can_grab_plank(self):
        '''Returns boolean whether or not there is a held plank'''
        return not self.held_plank

    def add_planks(self, planks):
        '''Adds planks to the set of planks'''
        for plank in planks:
            self.add_plank(plank)

    def add_plank(self, plank):
        '''Adds a plank to the set of planks; updates the covered points'''
        self.planks.add(plank)
        self._covered_points = self._covered_points.union(get_waypoints(plank))

    def add_pegs(self, pegs):
        '''Adds pegs to the set of pegs'''
        for peg in pegs:
            self.add_peg(peg)

    def add_peg(self, peg):
        '''Add a peg to the set of pegs'''
        self.pegs.add(peg)

    def remove_plank(self, plank):
        '''Removes a plank from the set of planks; updates the covered points'''
        self.planks.remove(plank)
        self._covered_points = self._covered_points.difference(get_waypoints(plank))


def get_waypoints(plank):
    '''Gets the points that are not the endpoints of the plank'''
    ans = set()
    direction, total_distance = get_peg_direction_dist(*plank)
    if direction is None:
        return ans
    for path_distance in range(1, total_distance):
        ans.add(get_peg_in_direction(plank[0], direction, how_many=path_distance))
    return ans

def get_plank(peg1, peg2):
    '''Takes two endpoints and returns a plank between those two endpoints'''
    # a plank is represented by a sorted tuple of the pegs its between
    return tuple(sorted([peg1, peg2]))

def get_peg_dist(peg1, peg2):
    '''
    Gets the distance between two pegs.
    Diagonal distance is undefined - this function will return None
    '''
    # the (peg - 1) part is needed because we need peg 15 to be on the same row as peg 11
    # (In other words, the pegs aren't 0 indexed so it's causing problems)
    peg1_mod = (peg1 - 1) % WIDTH
    peg2_mod = (peg2 - 1) % WIDTH
    abs_dist = abs(peg2 - peg1)
    if peg1_mod == peg2_mod:
        # they're in the same column
        return abs_dist // WIDTH
    else:
        # they're not in the same column
        if peg1 - peg1_mod == peg2 - peg2_mod:
            # they're in the same row
            return abs_dist
        else:
            # they're not in the same column or row; distance is undefined
            return None

def get_peg_direction_dist(peg1, peg2):
    '''
    Returns the direction from peg1 to peg2 and the distance between them as a tuple

    Form: (direction, distance)
    '''

    # upgrade: this code is very similar to get_peg_dist
    # the (peg - 1) part is needed because we need peg 15 to be on the same row as peg 11
    # (In other words, the pegs aren't 0 indexed so it's causing problems)
    peg1_mod = (peg1 - 1) % WIDTH
    peg2_mod = (peg2 - 1) % WIDTH
    abs_dist = abs(peg2 - peg1)
    peg2_bigger = max((peg1, peg2)) == peg2
    if peg1_mod == peg2_mod:
        # they're in the same column
        direction = 2 if peg2_bigger else 0
        return direction, abs_dist // WIDTH
    else:
        # they're not in the same column
        if peg1 - peg1_mod == peg2 - peg2_mod:
            direction = 1 if peg2_bigger else 3
            # they're in the same row
            return direction, abs_dist
        else:
            # they're not in the same column or row; distance is undefined
            return None, None


def get_peg_in_direction(peg, direction, how_many=1): # pylint: disable=inconsistent-return-statements
    '''Returns the peg the given number of steps away from the given peg in the given direction'''
    if how_many > 1:
        peg = get_peg_in_direction(peg, direction, how_many - 1)

    if peg is None:
        return None

    if direction == UP:
        if peg > WIDTH:
            # peg not on top
            return peg - WIDTH

    elif direction == RIGHT:
        if peg % WIDTH:
            # not on the right
            return peg + 1

    elif direction == DOWN:
        if peg <= WIDTH * (HEIGHT - 1):
            # not on bottom
            return peg + WIDTH

    elif direction == LEFT:
        if peg % WIDTH != 1:
            # not on the left
            return peg - 1

    else:
        raise ValueError("Unrecognized direction: {}".format(direction))

def count_grab_and_place(moves):
    '''Counts how many grab moves and place moves combined there are. Useful for debugging.'''
    counter = 0
    for move_type, peg in moves: # pylint: disable=unused-variable
        if move_type in ('grab', 'place'):
            counter += 1
    return counter

def take_out_walk_moves(moves):
    '''Takes out any walk moves from a solution'''
    return [move for move in moves if move[0] != 'walk']
