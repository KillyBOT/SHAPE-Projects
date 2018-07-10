import time
import math

goalState1 = ((0,1,2),(3,4,5),(6,7,8))
goalState2 = ((1,2,3),(4,5,6),(7,8,0))
goalStates = [goalState1, goalState2]

#Pick 0 for goal state 1, pick 1 for goal state 2

goal = 1

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)
    
def get_zero_position(state):
    zeroPos = 0

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] == 0:
                return row, column

def get_num_position(state,num):
    numPos = 0

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] == num:
                return row, column
                break

def get_successors(state):
    child_states = []

    zeroPos = get_zero_position(state)

    tupleToAdd = []
    if zeroPos[0] > 0:
        tupleToAdd.append("Up")
        tupleToAdd.append(tuple(swap_cells(state,zeroPos[0],zeroPos[1],zeroPos[0]-1,zeroPos[1])))
        child_states.append(tuple(tupleToAdd))
        tupleToAdd = []

    if zeroPos[0] < len(state) - 1:
        tupleToAdd.append("Down")
        tupleToAdd.append(tuple(swap_cells(state,zeroPos[0],zeroPos[1],zeroPos[0]+1,zeroPos[1])))
        child_states.append(tuple(tupleToAdd))
        tupleToAdd = []

    if zeroPos[1] > 0:
        tupleToAdd.append("Left")
        tupleToAdd.append(tuple(swap_cells(state,zeroPos[0],zeroPos[1],zeroPos[0],zeroPos[1]-1)))
        child_states.append(tuple(tupleToAdd))
        tupleToAdd = []

    if zeroPos[1] < len(state) - 1:
        tupleToAdd.append("Right")
        tupleToAdd.append(tuple(swap_cells(state,zeroPos[0],zeroPos[1],zeroPos[0],zeroPos[1]+1)))
        child_states.append(tuple(tupleToAdd))
        tupleToAdd = []

    
    return child_states

            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """    

    #YOUR CODE HERE

    return state==goalStates[goal]
   
def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    parents = {}
    actions = {}

    states_expanded = 0
    max_frontier = 0

    frontier = [state]
    seen = set()
    seen.add(state)

    while goal_test(frontier[0]) == False:
        states_expanded += 1
        max_frontier = len(frontier)
        for newState in get_successors(frontier[0]):
            if newState[1] not in seen:
                frontier.append(newState[1])
                parents[newState[1]] = frontier[0]
                seen.add(newState[1])
                actions[newState[1]] = newState[0]
        frontier.pop(0)
        if len(frontier) <= 0:
            return None, states_expanded, max_frontier
            break

    currentState = frontier[0]
    listOfActions = []

    while currentState != state:
        listOfActions.insert(0, actions[currentState])
        currentState = parents[currentState]

    return listOfActions, states_expanded, max_frontier
                               
     
def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """

    parents = {}
    actions = {}

    states_expanded = 0
    max_frontier = 0

    frontier = [state]
    seen = set()
    seen.add(state)

    while len(frontier) > 0:
        states_expanded += 1
        max_frontier = len(frontier)
        topOfStack = frontier.pop()
        if goal_test(topOfStack) == True:
            currentState = topOfStack
            listOfActions = []

            while currentState != state:
                listOfActions.insert(0, actions[currentState])
                currentState = parents[currentState]

            return listOfActions, states_expanded, max_frontier
        amountOfSeenTiles = 0
        for newState in get_successors(topOfStack):
            if newState[1] not in seen:
                parents[newState[1]] = topOfStack
                seen.add(newState[1])
                actions[newState[1]] = newState[0]
                frontier.append(newState[1])

    return None, states_expanded, max_frontier
            


def misplaced_heuristic(state, goalState):
    """
    Returns the number of misplaced tiles.
    """

    #YOUR CODE HERE

    amountOfMisplacedTiles = 0

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] != goalState[row][column]:
                amountOfMisplacedTiles += 1

    return amountOfMisplacedTiles


def manhattan_heuristic(state, goalState):
    """
    For each misplaced tile, compute the manhattan distance between the current
    position and the goal position. Then sum all distances. 
    """
    amountOfMisplacedTiles = 0
    zeroPos = get_zero_position(state)

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] != goalState[row][column] and state[row][column] != 0:
                currentNumPos = get_num_position(state,goalState1[row][column])
                amountOfMisplacedTiles += int(abs(zeroPos[0] - currentNumPos[0]))
                amountOfMisplacedTiles += int(abs(zeroPos[1] - currentNumPos[1]))
                #print(goalState1[row][column])
                #print(goalState2[row][column])

    return amountOfMisplacedTiles


def best_first(state):
    """
    Depth first search using the heuristic function passed as a parameter.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """

    # You might want to use these functions to maintain a priority queue
    import heapq

    parents = {}
    actions = {}
    heuristic = {}

    heuristicHeap = []

    heuristic[state] = manhattan_heuristic(state, goalStates[goal])

    states_expanded = 0
    max_frontier = 0

    frontier = [(heuristic[state], state)]
    heapq.heapify(frontier)
    seen = set()
    seen.add(state)

    while len(frontier) > 0:
        states_expanded += 1
        max_frontier = len(frontier)
        topOfStack = heapq.heappop(frontier)[1]
        if goal_test(topOfStack) == True:

            currentState = topOfStack
            listOfActions = []

            while currentState != state:
                listOfActions.insert(0, actions[currentState])
                currentState = parents[currentState]

            return listOfActions, states_expanded, max_frontier

        for newState in get_successors(topOfStack):
            if newState[1] not in seen:
                heuristic[newState[1]] = manhattan_heuristic(newState[1], goalStates[goal])
                parents[newState[1]] = topOfStack
                seen.add(newState[1])
                actions[newState[1]] = newState[0]
                heapq.heappush(frontier, (heuristic[newState[1]], newState[1]))

    return None, states_expanded, max_frontier

    #YOUR CODE HERE

    # The following line computes the heuristic for a state
    # by calling the heuristic function passed as a parameter. 
    # f = heuristic(state) 

    #  return solution, states_expanded, max_frontier

def astar(state):
    """
    A-star search using the heuristic function passed as a parameter. 
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.  
    """
    # You might want to use these functions to maintain a priority queue

    import heapq

    parents = {}
    actions = {}
    heuristic = {}
    cost = {}
    total = {}

    heuristic[state] = manhattan_heuristic(state, goalStates[goal])
    cost[state] = 0
    
    states_expanded = 0
    max_frontier = 0

    frontier = [(heuristic[state], state)]
    heapq.heapify(frontier)
    seen = set()
    seen.add(state)

    while len(frontier) > 0:
        states_expanded += 1
        max_frontier = len(frontier)
        topOfStack = heapq.heappop(frontier)[1]
        if goal_test(topOfStack) == True:

            currentState = topOfStack
            listOfActions = []

            while currentState != state:
                listOfActions.insert(0, actions[currentState])
                currentState = parents[currentState]

            return listOfActions, states_expanded, max_frontier

        for newState in get_successors(topOfStack):
            if newState[1] not in seen:

                cost[newState[1]] = cost[topOfStack] + 1
                heuristicToAdd = cost[newState[1]] + manhattan_heuristic(newState[1],goalStates[goal])
                heuristic[newState[1]] = heuristicToAdd

                parents[newState[1]] = topOfStack
                seen.add(newState[1])
                actions[newState[1]] = newState[0]
                heapq.heappush(frontier, (heuristic[newState[1]], newState[1]))

    return None, states_expanded, max_frontier # No solution found


def print_result(solution, states_expanded, max_frontier):
    """
    Helper function to format test output. 
    """
    if solution is None: 
        print("No solution found.")
    else: 
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max frontier size: {}.".format(max_frontier))

def print_actions(solution, state):

    newState = state

    for action in range(len(solution)):
        zeroPos = get_zero_position(newState)
        print("Step %d:" % (action+1))
        if solution[action] == "Up":
            newState = swap_cells(newState, zeroPos[0], zeroPos[1], zeroPos[0] - 1, zeroPos[1])
            print(state_to_string(newState))
            print("Move Zero Up\n")
        elif solution[action] == "Down":
            newState = swap_cells(newState, zeroPos[0], zeroPos[1], zeroPos[0] + 1, zeroPos[1])
            print(state_to_string(newState))
            print("Move Zero Down\n")
        elif solution[action] == "Left":
            newState = swap_cells(newState, zeroPos[0], zeroPos[1], zeroPos[0], zeroPos[1] - 1)
            print(state_to_string(newState))
            print("Move Zero Left\n")
        elif solution[action] == "Right":
            newState = swap_cells(newState, zeroPos[0], zeroPos[1], zeroPos[0], zeroPos[1] + 1)
            print(state_to_string(newState))
            print("Move Zero Right\n")