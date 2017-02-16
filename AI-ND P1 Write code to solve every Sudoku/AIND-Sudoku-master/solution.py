
# We create a new list to store the assignments
assignments = []

# Lession material showed us to use this variabeles and functions:
rows = 'ABCDEFGHI'
cols = '123456789'
width = len(rows)

# Define cross function, we had to change a, b into A, B thus we are using caps now, in class we did not
def cross(A, B):
    return [s+t for s in A for t in B]
	
	  
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]	  
diag_units = [ [ row[idx] for idx, row in enumerate(row_units) ],
               [ row[width - idx - 1] for idx, row in enumerate(row_units) ] ]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    out = {k:v for k,v in values.items()}
    for unit in unitlist:
        bidigits = {}
        ntwins   = {}
        # Find all pairs of naked twins
        for box in unit:
            val = values[box]
            # do only for values with two digits
            if len(val) == 2:
                if val in bidigits:
                    # Found a naked twin pair
                    ntwins[val] = (box, bidigits[val])
                else:
                    # Found just one box with two digit value
                    bidigits[val] = box
        # For each naked twin pair, reduce the possibilities of other boxes in the unit.
        # Reduction is done based on the observation that the "other" boxes in the unit
        # cannot have the digits present in the naked twins.
        for twinval, tboxes in ntwins.items():
            # Find set of other boxes in the unit
            others = set(unit) - set(tboxes)
            for other in others:
                oldval = values[other]
                # Remove both digits of twin pair from other boxes
                newval = oldval.replace(twinval[0], '').replace(twinval[1], '')
                if newval != oldval:
                    out = assign_value(out, other, newval)
    return out

# I copied this code from the class assignments
def grid_values(grid):
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

	
# I copied this code from the class assignments
def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# I copied this code from the class assignments
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values

# I copied this code from the class assignments
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

# I copied this code from the class assignments
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        # Call naked twins strat to reduce search space
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# I copied this code from the class assignments
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# I copied this code from the class assignments
def solve(grid):
    if isinstance(grid, str):
        # If input is just a string representation, then convert
        # to dict form
        grid = grid_values(grid)
    return search(grid)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
