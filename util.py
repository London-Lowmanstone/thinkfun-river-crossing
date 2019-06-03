'''Utility functions'''
from framework import get_plank

def invert_dictionary(mapping):
    '''
    Inverts a dictionary
    from https://stackoverflow.com/a/483833/
    '''
    return {v: k for k, v in mapping.items()}

def convert_to_rc_solution(solution, translator, starting_person_position):
    '''
    Takes a solution, a translator from pegs to RC characters,
    ...and a peg number for the starting person position,
    ...and returns the River Crossing solution string for that solution.
    '''
    def plank_converter(plank):
        ans = ""
        for peg in plank:
            ans += translator[peg].upper()

        return "".join(sorted(ans))

    ans = ""
    person_position = starting_person_position
    for move_type, peg in solution:
        if move_type == "walk":
            person_position = peg
        elif move_type == "grab":
            ans += plank_converter(get_plank(peg, person_position)) + '-'
        elif move_type == "place":
            ans += plank_converter(get_plank(peg, person_position)) + ' '
        else:
            raise ValueError("Unrecognized move type {}".format(move_type))

    return ans.strip()

class SolutionStepper: # pylint: disable=too-few-public-methods
    '''
    Class for stepping through River Crossing solution strings -
    Helpful for debugging
    '''
    def __init__(self, base_board_creator, solution_string, translator):
        '''
        Takes a function that creates a board when called with no parameters
        ...and a River Crossing solution string,
        ...and a translator from pegs to RC solution characters
        '''
        # when called, creates the board after 0 steps
        self.base_board_creator = base_board_creator
        solution_string = solution_string.strip().upper()
        self.moves = solution_string.split()
        self.moves = [move.split('-') for move in self.moves]
        self.moves = [tuple([get_plank(*[translator[peg] for peg in plank])
                             for plank in move])
                      for move in self.moves]

    def get_puzzle_at_step(self, step):
        '''
        Returns the puzzle after doing the given amount of steps
        ...from the River Crossing string
        '''
        ans = self.base_board_creator()
        for index in range(step):
            grab_plank, place_plank = self.moves[index]
            ans.remove_plank(grab_plank)
            ans.add_plank(place_plank)
            ans.person_position = place_plank[0]

        return ans
