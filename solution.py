from utils import *


assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def foundTwin(values, unit, box):
    """
    Returns if finds a twin
    Args:
        values(dict): The sudoku in dictionary form
        unit: The unit that we should look a twin
        box: The initial box "brother" that could have a twin
    """
    result = False
    value = values[box]

    if len(values[box]) == 2:
        for other in unit:
            if values[other] == value and other != box:
                result = True

    return result

def remove_twins(values, unit, box):
    """
    Twin found now it's time to remove it
    Args:
        values(dict): The sudoku in dictionary form
        unit: The unit that twin should be removed
        box: The initial box "brother" that have a twin
    """
    value = values[box]

    for peer in unit:
        if values[peer] != value:
            assign_value(values, peer, values[peer].replace(value[0],'').replace(value[1],''))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for unit in unitlist:
        for box in unit:
            if foundTwin(values, unit,box):
                remove_twins(values, unit, box)
    
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'

    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    return dict(zip(boxes, values))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]

        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]

            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)

    return values

def count_solved_boxes(values):
    """
    Count the number of solved values (box with value 1)
    Args: values(dict): The sudoku in dictionary form

    """
    return len([box for box in values.keys() if len(values[box]) == 1])

def reduce_puzzle(values):
    """
    Iterate through the puzzle applying the created strategies
    in order to solve the sudoku board
    Args: values(dict): The sudoku in dictionary form
    """
    stalled = False

    while not stalled:
        solved_values_before = count_solved_boxes(values)

        values = eliminate(values)

        values = only_choice(values)

        values = naked_twins(values)

        solved_values_after = count_solved_boxes(values)

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box])==0]):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    
    # Choose one of the unfilled squares with the fewest possibilities
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    values = reduce_puzzle(values)

    if values is False:
        return False

    
    if all(len(values[s])==1 for s in boxes):
      
      return values ##Solved!

    n, s = min((len(values[s]),s) for s in boxes if len(values[s]) >1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt: 
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    

    return search(values)

if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
