import os
from z3 import Optimize, Int, Sum, sat


# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day10_input.txt')
lines = input.readlines()
input.close()
lines = [line.strip() for line in lines]

def press_button(lights, button_lights):
    result = list(lights)
    for light in button_lights:
        if result[light] == '.':
            result[light] = '#'
        else:
            result[light] = '.'
    return "".join(result)

def count_presses(goal_lights, buttons):
    presses = 1
    states = set(['.' * len(goal_lights)])
    min_presses_map = dict()
    min_presses_map['.' * len(goal_lights)] = 0
    while True:
        next_states = set()
        for state in states:
            for button in buttons:
                new_lights = press_button(state, button)
                if new_lights == goal_lights:
                    return presses
                else:
                    if new_lights not in min_presses_map:
                        next_states.add(new_lights)
                        min_presses_map[new_lights] = presses
        presses += 1
        states = next_states.copy()

"""
-- This was my original implementation, but this takes too long for part 2.

def press_joltage_button(joltages, button):
    result = list(joltages)
    for number in button:
        result[number] += 1
    return tuple(result)

def overloaded(joltages, goal_joltages):
    for x in range(len(joltages)):
        if joltages[x] > goal_joltages[x]:
            return True
    return False

def count_joltage(goal_joltages, buttons):
    presses = 1
    states = set()
    states.add(tuple([0] * len(goal_joltages)))
    min_presses_map = dict()
    min_presses_map[tuple([0] * len(goal_joltages))] = 0
    while True:
        if len(states) == 0:
            return
        next_states = set()
        for state in states:
            for button in buttons:
                new_joltages = press_joltage_button(state, button)
                if new_joltages == goal_joltages:
                    return presses
                else:
                    if new_joltages not in min_presses_map and not overloaded(new_joltages, goal_joltages):
                        next_states.add(new_joltages)
                        min_presses_map[new_joltages] = presses
        presses += 1
        states = next_states.copy()

-- Attempt #2 took me through the dynamic programming route. Which worked for the example, but again, too slow for the real input

# Time for some dynamic programming!
def count_joltage_dp(goal_joltages, buttons):
    
    # To start with, we have no buttons pressed, with a cost of 0 and a state of 0s across the board
    # e.g. [{(0, 0, 0, 0): 0}] -- The 'state' is (0,0,0,0) and the 'cost' to reach this state is 0
    current_dict = {tuple([0] * len(goal_joltages)): 0}

    # For each button, calculate what states we can reach by pressing it 0...n times (where n is the limit before overloading the joltages)
    for button in buttons:

        print(len(current_dict))

        next_dict = {}

        # Start at each valid state we were able to reach from the previous buttons
        for state in current_dict:

            # Figure out how many times we can press this button without overflowing a joltage from this state
            max_button_presses = math.inf
            for number in button:
                max_button_presses = min(max_button_presses, goal_joltages[number] - state[number])
            
            # Compute the valid states we can reach by pressing this button 0...n times
            for presses in range(0, max_button_presses + 1):
                new_state = list(state)
                for number in button:
                    new_state[number] += presses
                new_cost = current_dict[state] + presses
                new_state = tuple(new_state)

                # Track if this is the first time we've seen this state, or if this is a cheaper number of presses to reach this state
                if new_state not in next_dict or next_dict[new_state] > new_cost:
                    next_dict[new_state] = new_cost
        
        # Shift dictionaries, it's time to take the next button into consideration
        current_dict = next_dict.copy()

    # By the end of this, we should have taken all possible button combinations into account
    # As long as the goal set of joltages is possible, we should know the optimal cost to find it at this point
    return current_dict[goal_joltages]
"""

# After conferring with the subreddit at 2:30 AM, I saw most of them were using Z3
# Which I honestly had forgotten about since using it once back in Advent of Code 2023
# This is a system of linear equations to be solved
def z3_save_me(goal_joltages, buttons):

    # Optimize instead of Solve, since we want to minimize the number of button presses (from multiple possible solutions)
    opt = Optimize()

    # Declare our variables -- how many times to press each button
    # Declare them as Int so we only get whole number solutions
    button_press_counts = []
    for x in range(len(buttons)):
        button_press_counts.append(Int(f"press_button_{x}"))

    # Constraint #1 - They must be positive numbers (can't unpress a button)
    for button in button_press_counts:
        opt.add(button >= 0)

    # Constraint #2 - The buttons need to match the correct joltages
    for light in range(len(goal_joltages)):
        connected_buttons = []
        for x in range(len(buttons)):
            if light in buttons[x]:
                connected_buttons.append(button_press_counts[x])
        total_joltage = Sum(connected_buttons)
        opt.add(total_joltage == goal_joltages[light])

    # Optimization #1 - We want to minimize the total button presses
    total_presses = Sum(button_press_counts)
    opt.minimize(total_presses)

    # This operation runs linear algebra methods and returns 'sat' if it found a solution successfully
    if opt.check() != sat:
        return None

    # Grab and return the minimized total presses that we asked for
    m = opt.model()
    return m.eval(total_presses).as_long()

ans = 0
ans2 = 0
for line in lines:
    line = line.split()
    goal_lights = line[0][1:-1]
    buttons = []
    for button in line[1:-1]:
        button = tuple([int(val) for val in button[1:-1].split(",")])
        buttons.append(button)
    presses = count_presses(goal_lights, buttons)
    ans += presses

    goal_joltages = tuple([int(val) for val in line[-1][1:-1].split(",")])
    presses = z3_save_me(goal_joltages, buttons)
    ans2 += presses
    
print("The fewest number of button presses needed to match the desired light indicators is", ans)
print("The fewest number of button presses needed to match the desired joltages is", ans2)