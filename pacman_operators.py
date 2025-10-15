'''
The Packman Problem
AI lab
'''    

import copy 

""" Helper functions for checking operator's conditions """

def print_state(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            print(state[i][j], end=" ")
        print()

def can_eat(state):
    for i in range(len(state)):
        if state[i][0]=='p' and state[i][1]=='f':  
            return 1  

def can_move_right(state):
    for i in range(len(state)):
        if state[i][0] == 'p':
            return not state[i][1] == 'p'
    return False


def can_move_left(state):
    for i in range(len(state)):
        if state[i][0] == 'p':
            return not state[0][0]=='p'
    return False


#def can_move_up(state):
#    for i in range(len(state)):
#        if state[]

""" Operator function: eat, move right, move left """

def eat(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'p':
                print("pacman found")
    return state



def move_right(state):
    if can_move_right(state):
        for i in range(len(state)):
            if state[i][0]=='p':
                state[i][0]=''
                state[i+1][0]='p'
                return state
    else: 
        return state
         
def move_left(state):
    if can_move_left(state):
        for i in range(len(state)):
            if state[i][0]=='p':
                state[i][0]=''
                state[i-1][0]='p'
                return state
    else:
        return state

def move_up(state):
    if can_move_up(state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'p':
                    state[i][j] = ''
                    state[i-1][j] = 'p'
                    return state
    else:
        return state




from itertools import zip_longest

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

initial_state = [    ['f',''],
    ['f',''],
    ['p','f'],
    ['',''],
    ['',''],
    ['',''],
    ['','f'],
    ['','']
]

initial_state = list(grouper(initial_state, 2))

#print(eat(initial_state))
#print(move_left(initial_state))
#print(move_right(initial_state))
for row in (initial_state):
    for element in row:
        print(element, end=' ')
    print()


state = initial_state
state = move_right(state)
state = eat(state)
print_state(state)
