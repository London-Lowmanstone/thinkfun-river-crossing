'''
Main program to show how to use this.
See terms.txt for definitions and explanations.
'''

if __name__ == "__main__":
    # pylint doesn't like the fact that my variables are lowercase here
    # pylint: disable=invalid-name
    from solvers import BFSSolver
    from puzzles import Expert39, Expert40, EXPERT40_TRANSLATOR, EXPERT40_SOLUTION
    from util import convert_to_rc_solution, SolutionStepper, invert_dictionary
    puzzle = Expert39()
    solver = BFSSolver()
    solution = solver.solve(puzzle)
    print("Solution to Expert Puzzle #39: {}".format(solution))

    puzzle = Expert40()
    solver = BFSSolver()
    # this takes around 10 seconds on my computer
    solution = solver.solve(puzzle)
    print("Solution to Expert Puzzle #40: {}".format(solution))
    # solving the puzzle does not edit the puzzle,
    # ...so we can get the starting position from it.
    rc_solution = convert_to_rc_solution(solution, EXPERT40_TRANSLATOR, puzzle.person_position)
    # note that this solution differs slightly from the booklet solution, but it works
    # I believe this solution has less walk moves, which is why the BFS solver finds it first
    print("River Crossing solution to Expert Puzzle #40: {}".format(rc_solution))

    my_stepper = SolutionStepper(Expert40, rc_solution,
                                 invert_dictionary(EXPERT40_TRANSLATOR))
    # the puzzle after 26 RC moves
    my_puzzle_after_moves = my_stepper.get_puzzle_at_step(26)
    print("The board after 26 moves of my solution: {}".format(my_puzzle_after_moves))

    real_stepper = SolutionStepper(Expert40, EXPERT40_SOLUTION,
                                   invert_dictionary(EXPERT40_TRANSLATOR))
    real_puzzle_after_moves = real_stepper.get_puzzle_at_step(26)
    print("The board after 26 moves of the real solution: {}".format(real_puzzle_after_moves))

    # the solutions are not equivalent
    assert my_puzzle_after_moves != real_puzzle_after_moves

    # determine at what step my solution and the real solution diverge
    # note that you can also determine this just by looking at the solution strings
    # ...but this provides more of a tutorial
    my_puzzle_after_moves, real_puzzle_after_moves = None, None
    diverge_step = -1
    while my_puzzle_after_moves == real_puzzle_after_moves:
        diverge_step += 1
        my_puzzle_after_moves = my_stepper.get_puzzle_at_step(diverge_step)
        real_puzzle_after_moves = real_stepper.get_puzzle_at_step(diverge_step)

    print("My solution and the real solution diverge at step {}".format(diverge_step))
