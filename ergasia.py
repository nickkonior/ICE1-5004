import copy
import heapq
import sys

# Set recursion limit for deep searches
sys.setrecursionlimit(10**6)

# Initialize global variables
find_children_counter = 0
states_found = set()
operators_used = []
solution_found = False

# Operators for transition
def move_to_floor(state, target_floor):
    global operators_used
    current_floor, *floors, residents_in_elevator = state

    if current_floor == target_floor:
        return state

    residents_to_move = min(floors[target_floor - 1], 8 - residents_in_elevator)
    floors[target_floor - 1] -= residents_to_move
    residents_in_elevator += residents_to_move
    operators_used.append(f"move_to_floor: {target_floor}")
    
    return [target_floor] + floors + [residents_in_elevator]

def determine_next_move(state):
    current_floor, *floors, residents_in_elevator = state

    # Check if elevator should go to the roof
    if residents_in_elevator == 8 or not any(floors[current_floor:]):
        return [5] + floors + [residents_in_elevator]

    # Find the next floor with residents
    for next_floor in range(current_floor + 1, 5):
        if floors[next_floor - 1] > 0:
            return move_to_floor(state, next_floor)

    return state

def release_capacity(state):
    if state[0] == 5:
        # Reset the number of residents in the elevator to 0 when on the roof
        return [5] + state[1:5] + [0]
    return state

# Function to find children of the current state
def find_children(state):
    global find_children_counter
    global states_found
    find_children_counter += 1
    children = []

    next_move_state = determine_next_move(copy.deepcopy(state))
    if next_move_state != state:
        children.append(next_move_state)

    release_capacity_state = release_capacity(copy.deepcopy(state))
    if release_capacity_state != state:
        children.append(release_capacity_state)
        for floor in range(1, 5):
            if release_capacity_state[floor] > 0:
                return_to_floor_state = move_to_floor(release_capacity_state, floor)
                children.append(return_to_floor_state)
                break

    for child_state in children:
        states_found.add(tuple(child_state))

    return children

# Function to create the front for the search
def make_front(state):
    return [state]

# Function to expand the front based on the search method
def expand_front(front, method):
    if method == 'DFS':
        if front:
            node = front.pop(0)
            for child in find_children(node):
                front.insert(0, child)
    elif method == 'BFS':
        if front:
            node = front.pop(0)
            for child in find_children(node):
                front.append(child)
    elif method == 'BestFS':
        if front:
            node = heapq.heappop(front)
            for child in find_children(node):
                heapq.heappush(front, child)
    return front

# Function to create the queue for the search
def make_queue(state):
    return [[state]]

# Function to extend the queue based on the search method
def extend_queue(queue, method):
    if method == 'DFS':
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.insert(0, path)
    elif method == 'BFS':
        node = queue.pop(0)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)
    elif method == 'BestFS':
        node = heapq.heappop(queue)
        queue_copy = copy.deepcopy(queue)
        children = find_children(node[-1])
        for child in children:
            path = copy.deepcopy(node)
            path.append(child)
            heapq.heappush(queue_copy, path)
    return queue_copy

# Recursive function to create the search tree and find a solution
def find_solution(front, queue, closed, goal, method):
    global solution_found
    
    if not front:
        print('_NO_SOLUTION_FOUND_')
        return
    
    current_state = tuple(front[0])  # Convert list to tuple for hashing
    if current_state == tuple(goal):  # Convert goal list to tuple as well
        print('_GOAL_FOUND_')
        print(queue[0])
        solution_found = True
        return
    
    if current_state not in closed:
        closed.add(current_state)
        front_children = expand_front(copy.deepcopy(front), method)
        queue_children = extend_queue(copy.deepcopy(queue), method)
        find_solution(front_children, queue_children, closed, goal, method)

# Main function to execute the code
def main():
    initial_state = [0, 9, 4, 12, 7, 0]
    goal = [5, 0, 0, 0, 0, 0]
    method = 'BFS'  # Default method

    method_input = input("Select the search method (DFS, BFS, BestFS): ").strip()
    if method_input in ['DFS', 'BFS', 'BestFS']:
        method = method_input
    else:
        print("Invalid method selected. Using BFS by default.")

    print('____BEGIN__SEARCHING____')
    find_solution(make_front(initial_state), make_queue(initial_state), set(), goal, method)
    print(f"'find_children' was called {find_children_counter} times.")
    print(f"Operators Used: {operators_used}")
    print(f"Unique States Found: {len(states_found)}")
    print(f"Solution Found: {'Yes' if solution_found else 'No'}")
    

if __name__ == "__main__":
    main()
