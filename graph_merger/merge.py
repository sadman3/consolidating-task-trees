# from utils import get_singular_form, get_utensils
from FOON_class import FunctionalUnit, Object
import os
import json
import pickle
from utils import get_utensils

utensils = get_utensils()
PHYSICAL_STATE_TRANSITION = json.load(
    open("transition_model/physical_state_transitions.json", "r"))
# -----------------------------------------------------------------------------------------------------------------------------#


def is_grammar_ok(fu):
    if "input_nodes" not in fu:
        return False

    if "output_nodes" not in fu:
        return False

    if "motion_node" not in fu:
        return False

    return True

# -----------------------------------------------------------------------------------------------------------------------------#


def is_transition_ok(transition):
    for ing in transition:
        if len(transition[ing]) > 1:
            initial_state = transition[ing][0]
            final_state = transition[ing][1]

            if initial_state == final_state:
                continue

            else:
                found = False
                for states in PHYSICAL_STATE_TRANSITION:
                    for i in range(len(states)-1):
                        if states[i] == initial_state and states[i+1] == final_state:

                            found = True
                            break
                    if found:
                        break

                if not found:
                    print(transition[ing])
                    print()
                    return False
    return True
# -----------------------------------------------------------------------------------------------------------------------------#


def is_logic_ok(fu):
    transition = {}
    for node in fu["input_nodes"]:
        label = node["label"]
        transition[label] = []
        if label not in utensils:
            if len(node["states"]) > 0:
                physical_state = node["states"][0]

                transition[label].append(physical_state)

    for node in fu["output_nodes"]:
        label = node["label"]
        if label not in transition:
            continue

        if len(node["states"]) > 0:
            physical_state = node["states"][0]

            transition[label].append(physical_state)

    return is_transition_ok(transition)

# -----------------------------------------------------------------------------------------------------------------------------#


def is_valid_fu(fu):
    try:
        return is_grammar_ok(fu) and is_logic_ok(fu)
    except:
        return False


# merge different output of same recipe generated by finetuned model
def create_mini_foon(recipe_id):
    dir = "finetuned_output_corrected/JSON"

    mini_foon = []
    for i in range(1, 6):

        tree_path = os.path.join(dir, str(i), recipe_id + ".json")

        if not os.path.exists(tree_path):
            continue

        task_tree = json.load(open(tree_path))

        for fu in task_tree:
            if is_valid_fu(fu):
                mini_foon.append(fu)
    print(len(mini_foon))

    json.dump(mini_foon, open("mini_foon.json", "w"), indent=4)


# -----------------------------------------------------------------------------------------------------------------------------#


def get_FU_list(filepath="mini_foon.json"):
    """
        parameters: path of a subgraph text file
        returns: a list of FU
    """
    graph = json.load(open(filepath))

    FU_list = []

    for fu in graph:
        FU = FunctionalUnit()
        for item in fu['input_nodes']:
            new_object = Object(item["label"])
            new_object.states = item["states"]
            new_object.ingredients = item["ingredients"]
            new_object.container = item["container"]
            FU.input_nodes.append(new_object)

        for item in fu['output_nodes']:
            new_object = Object(item["label"])
            new_object.states = item["states"]
            new_object.ingredients = item["ingredients"]
            new_object.container = item["container"]
            FU.output_nodes.append(new_object)

        FU.motion_node = fu["motion_node"]

        FU_list.append(FU)
    return FU_list

# -----------------------------------------------------------------------------------------------------------------------------#


def save_to_pkl():
    """
        parameters: directory of subgraphs
        creates: a merged version of all subgraphs (universal FOON)
    """
    # # some subgraphs are not that good.
    # # excluding those subgraphs for better result
    # exclude_subgraph = ['0048-shrimp-mango_salad.txt']

    FU_list = get_FU_list()

    functional_units = []
    fu_id = 0

    for FU in FU_list:
        # checking duplicate functional unit
        if not FU.check_if_FU_exist(functional_units):
            FU.id = fu_id  # set the id according to its index
            functional_units.append(FU)
            fu_id += 1

    # save universal foon in a pickle file
    object_nodes = []
    object_id = 0
    for FU in functional_units:
        for _input in FU.input_nodes:
            # avoid adding duplicate objects
            existing_object_id = _input.check_object_exist(object_nodes)

            # if the object exists, assign the existing object id
            # if it does not, give it a new id
            if existing_object_id == -1:  # object is not found
                _input.id = object_id
                object_nodes.append(_input)
                object_id += 1
            else:
                _input.id = existing_object_id

        for _output in FU.output_nodes:
            existing_object_id = _output.check_object_exist(object_nodes)

            if existing_object_id == -1:  # object is not found
                _output.id = object_id
                object_nodes.append(_output)
                object_id += 1
            else:
                _output.id = existing_object_id

    object_to_FU_map = {}

    # create a mapping between output node to functional units
    # in this map, key = object index in object_nodes,
    # value = index of all FU where this object is an output
    for FU_index, FU in enumerate(functional_units):
        for _output in FU.output_nodes:

            # ignore object that has no state like "knife"
            if len(_output.states) == 0 and len(_output.ingredients) == 0 and _output.container == None:
                continue

            object_index = _output.id
            if object_index not in object_to_FU_map:
                object_to_FU_map[object_index] = []
            object_to_FU_map[object_index].append(FU_index)

    foon_pkl_path = "mini_foon.pkl"

    F = open(foon_pkl_path, "wb")
    pickle_data = {
        "functional_units": functional_units,
        "object_nodes": object_nodes,
        "object_to_FU_map": object_to_FU_map
    }
    pickle.dump(pickle_data, F)
    F.close()
    print('-- mini foon saved to', foon_pkl_path)

    print('-- total functional unit:', len(functional_units))


if __name__ == "__main__":
    for f in os.listdir("finetuned_output/JSON/1"):
        f = f.removesuffix(".json")
        create_mini_foon(f)
    # save_to_pkl()
