from collections import deque
import copy

class Action:
    def __init__(self, name, pre_pos, pre_neg, eff_pos, eff_neg):
        self.name = name
        self.pre_pos = set(pre_pos)
        self.pre_neg = set(pre_neg)
        self.eff_pos = set(eff_pos)
        self.eff_neg = set(eff_neg)

    def is_applicable(self, state):
        # Action is applicable if all positive preconditions are in the state
        # and no negative preconditions are in the state
        return self.pre_pos.issubset(state) and self.pre_neg.isdisjoint(state)

    def apply(self, state):
        # 1. Remove negative effects
        # 2. Add positive effects
        new_state = copy.deepcopy(state)
        new_state.difference_update(self.eff_neg)
        new_state.update(self.eff_pos)
        return frozenset(new_state)

def bfs_plan(initial_state, goal_state, actions):
    # State is represented as a frozenset of string propositions
    queue = deque([(frozenset(initial_state), [])])
    visited = set([frozenset(initial_state)])

    while queue:
        current_state, plan = queue.popleft()

        # Check if goal is satisfied in current state
        if set(goal_state).issubset(current_state):
            return plan, current_state

        # Find applicable actions and generate successor states
        for action in actions:
            if action.is_applicable(current_state):
                next_state = action.apply(current_state)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, plan + [action]))

    return None, None # No plan found

def run_test(test_name, initial_state, goal_state, actions):
    print(f"--- {test_name} ---")
    print(f"Initial: {initial_state}")
    print(f"Goal: {goal_state}")
    
    plan, final_state = bfs_plan(initial_state, goal_state, actions)
    
    if plan is None:
        print("Result: No plan found\n")
    else:
        print("Result: Plan found!")
        current = frozenset(initial_state)
        for step, action in enumerate(plan, 1):
            current = action.apply(current)
            print(f"  Step {step}: {action.name}")
            print(f"  State after step {step}: {set(current)}")
        print("\n")

if __name__ == "__main__":
    # Base Actions
    actions_base = [
        Action("Move(A, B)", ["At(Robot, A)"], [], ["At(Robot, B)"], ["At(Robot, A)"]),
        Action("Move(B, C)", ["At(Robot, B)"], [], ["At(Robot, C)"], ["At(Robot, B)"]),
        Action("Move(B, A)", ["At(Robot, B)"], [], ["At(Robot, A)"], ["At(Robot, B)"]),
        Action("Move(C, B)", ["At(Robot, C)"], [], ["At(Robot, B)"], ["At(Robot, C)"]),
        Action("PickUp(Package, A)", ["At(Robot, A)", "At(Package, A)"], ["Holding(Package)"], ["Holding(Package)"], ["At(Package, A)"]),
        Action("PickUp(Package, B)", ["At(Robot, B)", "At(Package, B)"], ["Holding(Package)"], ["Holding(Package)"], ["At(Package, B)"]),
        Action("PickUp(Package, C)", ["At(Robot, C)", "At(Package, C)"], ["Holding(Package)"], ["Holding(Package)"], ["At(Package, C)"]),
        Action("Drop(Package, A)", ["At(Robot, A)", "Holding(Package)"], [], ["At(Package, A)"], ["Holding(Package)"]),
        Action("Drop(Package, B)", ["At(Robot, B)", "Holding(Package)"], [], ["At(Package, B)"], ["Holding(Package)"]),
        Action("Drop(Package, C)", ["At(Robot, C)", "Holding(Package)"], [], ["At(Package, C)"], ["Holding(Package)"])
    ]

    initial = {"At(Robot, A)", "At(Package, A)"}
    goal = {"At(Package, C)"}

    # Test A: Solvable Problem
    run_test("Test A: Solvable Problem", initial, goal, actions_base)

    # Test B: Impossible Problem (Remove PickUp actions)
    actions_no_pickup = [a for a in actions_base if "PickUp" not in a.name]
    run_test("Test B: Impossible Problem", initial, goal, actions_no_pickup)

    # Test C: Irrelevant Actions 
    # The base logic already inherently handles irrelevant actions (moving without picking up) 
    # because the goal specifically requires At(Package, C), not At(Robot, C).
    run_test("Test C: Irrelevant Actions", initial, goal, actions_base)
