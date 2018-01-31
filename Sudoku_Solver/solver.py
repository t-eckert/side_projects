'''
    [row][col]
'''

import numpy as np 

# Loading, display, solving command, and checking if solved.

def load(filename):
    '''Given a puzzle file, this will load it into memory'''
    possible = [[[k for k in range(1,10)] for i in range(0,9)] for j in range(0,9)]
    known = [[0 for i in range(0,9)] for j in range(0,9)]
    load_p = np.loadtxt(filename, dtype=int, delimiter=',')
    print("%s is loaded into puzzle array" % filename)
    for i in range(0,9):
        for j in range(0,9):
            if load_p[9*i+j] != 0:
                possible[i][j] = [load_p[9*i+j]]
                known[i][j] = load_p[9*i+j]
    puzzle = (possible, known) 
    return puzzle

def pretty_print(puzzle):
    '''Takes in the puzzle object and prints it in a readable format.'''
    k = puzzle[1]
    i = 0
    for row in k:
        if i%3 == 0 and i != 0:
            print("---------------------")
        print("%s %s %s | %s %s %s | %s %s %s" % 
                (row[0], row[1], row[2], 
                 row[3], row[4], row[5], 
                 row[6], row[7], row[8]))
        i += 1
    pass

def solve(puzzle):
    puzzle, changed = reduce_possible(puzzle)
    # Check if the puzzle has changed.
    if changed == False:
        puzzle = reduce_unique(puzzle)
    return puzzle

def solved(puzzle):
    '''True if puzzle is solved. False otherwise.'''
    possible, known = puzzle
    for row in known:
        for val in row:
            if val == 0:
                return False
    return True
    
# Finds values in the Row, Column, and Group for known or possible lists.

def find_row_vals(all_vals):
    in_row = []
    for row in all_vals:
        in_row.append(row)
    return in_row

def find_col_vals(all_vals):
    in_col = []
    for i in range(0,9):
        col_vals = []
        for j in range(0,9):
            col_vals.append(all_vals[j][i])
        in_col.append(col_vals)
    return in_col

def find_grp_vals(all_vals):
    in_grp = [[] for m in range(0,9)]
    sect = [[0,1,2], [3,4,5], [6,7,8]]
    for i in range(0,9):
        for j in range(0,9):
            for x in range(0,3):
                for y in range(0,3):
                    if i in sect[x] and j in sect[y]:
                        in_grp[3*x +y].append(all_vals[i][j])
    return in_grp

def which_group(i,j):
    '''Gives a group number based on the coordinates'''
    sect = [[0,1,2], [3,4,5], [6,7,8]]
    for x in range(0,3):
        for y in range(0,3):
            if i in sect[x] and j in sect[y]:    
                return 3*x +y

# If the puzzle undergoes no change between two checks, try to reduce the 
# unknowns by finding where unique values are possible.

def reduce_possible(puzzle):
    '''Reduces unknowns by cancellation with other possibilities.'''
    changed = False
    possible, known = puzzle
    known_in_row = find_row_vals(known)
    known_in_col = find_col_vals(known)
    known_in_grp = find_grp_vals(known)
    #print(known_in_grp)
    for i in range(0,9):
        for j in range(0,9):
            if known[i][j] == 0:
                m = which_group(i,j)
                #print("[Row: %s][Col: %s]" % (i,j))
                poss = possible[i][j]
                #print("Row ->")
                poss = compare_to_known(poss, known_in_row[i])
                #print("Col ->")
                poss = compare_to_known(poss, known_in_col[j])
                #print("Grp ->")
                poss = compare_to_known(poss, known_in_grp[m])
                possible[i][j] = poss
                if len(poss) == 1:
                    known[i][j] = poss[0]
                    changed = True
    return puzzle, changed

def reduce_unique(puzzle):
    '''Reduce unknowns by finding uniquely possible values.'''
    unique, i, j = check_unique_row(find_row_vals(possible),find_row_vals(known))
    return puzzle

def compare_to_known(poss, know):
    for k in know:
        if k in poss:
            poss.remove(k)
    #print("Know %s; Possible %s" % (know,poss))
    return poss

def confirm_unique_values(puzzle):
    possible, known = puzzle

    poss_in_row = find_row_vals(possible)
    known_in_row = find_row_vals(known)
    unique_in_row = check_unique_possible(poss_in_row)
    new_unique_in_row = remove_knowns(unique_in_row,known_in_row)

    print(poss_in_row)
    print(new_unique_in_row)

    
    
    return puzzle

def check_unique_possible(poss):
    unique_in_set = []
    flat_poss = []
    for unit in poss:
        flat_poss.append([item for sublist in unit for item in sublist])
    for flat_unit in flat_poss:
        unit_unique = []
        for i in range(1,10):
            if flat_unit.count(i) == 1:
                unit_unique.append(i)
        unique_in_set.append(unit_unique)
    return unique_in_set

def remove_knowns(unique,known):
    for val in known:
        if val in unique:
            unique.remove(val)
    return unique

def main():
    puzzle = load('Puzzles/puzzle1.txt')
    pretty_print(puzzle)
    print()
    count = 0
    while not solved(puzzle):
        pretty_print(solve(puzzle))
        print()
        if count > 20:
            break 
        count += 1
    print(count)

main()