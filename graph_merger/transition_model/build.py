import os
import json

subgraph_dir = "../../../progress_line/subgraph"


def check_transition_exists(existing_transitions, new_transition):
    for item in existing_transitions:
        if sorted(item) == sorted(new_transition):
            return True

    return False


def build_physical_state_transition():
    transition_list = []
    for f in os.listdir(subgraph_dir):
        progress_line = json.load(open(os.path.join(subgraph_dir, f)))

        for item in progress_line:
            transitions = []
            for state in item["state"]:
                physical_state = state["physical_state"]
                if len(physical_state) > 0:
                    individual_states = physical_state.split(",")
                    for k in individual_states:
                        if k not in transitions:
                            transitions.append(k)

            if len(transitions) > 0 and check_transition_exists(transition_list, transitions) == False:
                transition_list.append(transitions)

    json.dump(transition_list, open(
        "physical_state_transitions.json", "w"), indent=4)


def build_physical_state_transition():
    transition_list = []
    for f in os.listdir(subgraph_dir):
        progress_line = json.load(open(os.path.join(subgraph_dir, f)))

        for item in progress_line:
            transitions = []
            for state in item["state"]:
                physical_state = state["physical_state"]
                if len(physical_state) > 0:
                    individual_states = physical_state.split(",")
                    for k in individual_states:
                        if k not in transitions:
                            transitions.append(k)

            if len(transitions) > 0 and check_transition_exists(transition_list, transitions) == False:
                transition_list.append(transitions)

    json.dump(transition_list, open(
        "physical_state_transitions.json", "w"), indent=4)


def test_state_transition(transitions):
    transition_model = json.load(open("physical_state_transitions.json", "r"))
    for i in range(len(transitions) - 1):
        state1 = transitions[i]
        state2 = transitions[i+1]

        print("evaluating:   {} --> {}".format(state1, state2))
        flag = True
        for states in transition_model:
            for j in range(len(states)-1):
                if states[j] == state1 and states[j+1] == state2:
                    print("\t\tValid\n")
                    flag = False
                    break
            if not flag:
                break

        if flag:
            print("\t\tInvalid\n")
            return


def build_motion_transition():
    transition_list = []
    for f in os.listdir(subgraph_dir):
        progress_line = json.load(open(os.path.join(subgraph_dir, f)))

        for item in progress_line:
            transitions = []
            for motion in item["motion"]:
                if motion not in transitions:
                    transitions.append(motion)

            if len(transitions) > 0 and check_transition_exists(transition_list, transitions) == False:
                transition_list.append(transitions)

    json.dump(transition_list, open(
        "motion_transitions.json", "w"), indent=4)


def build_location_transition():
    transition_list = []
    for f in os.listdir(subgraph_dir):
        progress_line = json.load(open(os.path.join(subgraph_dir, f)))

        for item in progress_line:
            transitions = []
            for state in item["state"]:
                physical_state = state["location"]
                if len(physical_state) > 0:
                    individual_states = physical_state.split(",")
                    for k in individual_states:
                        if k not in transitions:
                            transitions.append(k)

            if len(transitions) > 0 and check_transition_exists(transition_list, transitions) == False:
                transition_list.append(transitions)

    json.dump(transition_list, open(
        "location_transitions.json", "w"), indent=4)


# build_location_transition()
if __name__ == "__main__":
    # build_physical_state_transition()

    print("########################################################")

    transitions = ["whole", "peeled", "sliced"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["peeled", "whole", "sliced"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["whole", "cracked", "beaten"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["liquid", "hot"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["cooked", "raw"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["mixed", "partly cooked", "cooked", "folded"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["blended", "whole", "peeled"]

    test_state_transition(transitions)

    print("########################################################")

    transitions = ["whole", "peeled", "whirled"]

    test_state_transition(transitions)
