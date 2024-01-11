import os
import json
import pickle
import copy
from FOON_class import FunctionalUnit, Object
from utils import get_utensils
import itertools as IT
import collections
import shutil

MINI_FOON = pickle.load(open("mini_foon.pkl", "rb"))
foon_functional_units, foon_object_nodes, foon_object_to_FU_map = [], [], {}

utensils = get_utensils()
# Define goal node
GOAL_NODE = Object("blender")
GOAL_NODE.states = []
GOAL_NODE.ingredients = [
    "mango",
    "sugarpowder",
    "mango",
    "groundsugarpowder"
]
GOAL_NODE.container = None
#####

# -----------------------------------------------------------------------------------------------------------------------------#

# creates the graph using adjacency list
# each object has a list of functional list where it is an output


def read_universal_foon(filepath="mini_foon.pkl"):
    """
        parameters: path of universal foon (pickle file)
        returns: a map. key = object, value = list of functional units
    """
    pickle_data = pickle.load(open(filepath, 'rb'))
    functional_units = pickle_data["functional_units"]
    object_nodes = pickle_data["object_nodes"]
    object_to_FU_map = pickle_data["object_to_FU_map"]

    return functional_units, object_nodes, object_to_FU_map

# -----------------------------------------------------------------------------------------------------------------------------#


def find_goal_id(goal_node):
    object_nodes = MINI_FOON["object_nodes"]

    return goal_node.check_object_exist(object_nodes)


def search_one_path(goal_id):
    """
        parameters: a goal node

                    object_to_FU_map {
                        key = object index
                        value = list of index of functional units
                    }

                    function
        returns: a task tree that consists some functional units
    """

    print("Goal ID:", goal_id)

    # list of indices of functional units
    reference_task_tree = []

    # list of object indices that need to be searched
    items_to_search = []

    # find the index of the goal node in object node list
    items_to_search.append(goal_id)

    # list of item already explored
    items_already_searched = []

    while len(items_to_search) > 0:
        current_item_index = items_to_search.pop(0)  # pop the first element
        if current_item_index in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item_index)

        # current_item = foon_object_nodes[current_item_index]

        if current_item_index in foon_object_to_FU_map:

            candidate_units = foon_object_to_FU_map[current_item_index]

            best_candidate_idx = candidate_units[0]

            # if an fu is already taken, do not process it again
            if best_candidate_idx in reference_task_tree:
                continue

            reference_task_tree.append(best_candidate_idx)

            # all input of the selected FU need to be explored
            for node in foon_functional_units[best_candidate_idx].input_nodes:
                node_idx = node.id
                if node_idx not in items_to_search:

                    # if in the input nodes, we have bowl contains {onion} and onion, chopped, in [bowl]
                    # explore only onion, chopped, in bowl
                    flag = True
                    if node.label in utensils and len(node.ingredients) == 1:
                        for node2 in foon_functional_units[best_candidate_idx].input_nodes:
                            if node2.label == node.ingredients[0] and node2.container == node.label:

                                flag = False
                                break
                    if flag:
                        items_to_search.append(node_idx)

    # reverse the task tree
    reference_task_tree.reverse()

    # create a list of functional unit from the indices of reference_task_tree
    task_tree_units = []
    for i in reference_task_tree:
        # creating a copy to make sure that modifying a FU does not affect future search
        FU = copy.deepcopy(foon_functional_units[i])
        task_tree_units.append(FU.get_FU_as_json())

    output_path = open("output.json", "w")
    json.dump(task_tree_units, output_path, indent=4)

# -----------------------------------------------------------------------------------------------------------------------------#


def search_all_path(goal_id):
    foon_functional_units, foon_object_nodes, foon_object_to_FU_map = read_universal_foon()
    """
        parameters: a goal node

                    object_to_FU_map {
                        key = object index
                        value = list of index of functional units
                    }

                    function
        returns: a task tree that consists some functional units
    """

    print("Goal ID:", goal_id)
    root_nodes = foon_object_to_FU_map[goal_id]

    solutions = []
    all_path_trees = []

    for _root in root_nodes:
        print('\n  -- Starting root #' + str(root_nodes.index(_root)) + '...')

        # -- initialize the tree stack here for each root node:
        tree_stack = collections.deque()
        tree_stack.append(_root)

        # -- keep a list of all preliminary paths that we modify and build throughout the search:
        paths = collections.deque()
        paths.append([_root])

        # -- keep track of all items that have been evaluated for each path in the works:
        items_seen = {}
        items_seen[0] = set({goal_id})

        while tree_stack:
            head = tree_stack.popleft()

            permutations = set()

            inputs_evaluated = list()

            input_nodes = foon_functional_units[head].input_nodes

            for _input in input_nodes:

                input_index = _input.check_object_exist(foon_object_nodes)

                # -- for all inputs for the root FU node..
                candidates = None
                try:
                    # searchFOON = list of FU
                    # searchMap = object to FU map
                    candidates = [
                        I for I in foon_object_to_FU_map[input_index]]
                except KeyError:
                    pass
                # endtry

                if candidates:
                    temp_list = frozenset(candidates)
                    inputs_evaluated.append(input_index)
                    permutations.add(temp_list)

            if not permutations:
                continue

            new_children = set()
            for P in IT.product(*permutations):
                # Interesting note: set((1,2)) == set((2,1)) will be True, so this is why we don't have to worry!

                # -- add the tuples to the set, as it will only keep unique Cartesian sets:
                new_children.add(frozenset(P))
            # endfor

            # -- convert set of sets into list of lists for ease of use:
            new_children = [list(S) for S in new_children]

            # -- we will be making duplicates of existing paths (if they are relevant to this present head)
            # and add them to new_paths temporarily.
            new_paths = []
            new_items_seen = {}

            changes = False

            candidates_for_stack = set()

            print("path len", len(paths))
            if len(paths) > 1000:
                break

            for old_path in paths:

                if head in old_path:
                    # -- this means that a certain path has some relation to the head we are currently on:

                    for _set in new_children:
                        # --  a set is one of the computed Cartesian products from above:

                        # -- we take the record of what items have already been solved for a particular path:
                        temp_path = list(old_path)
                        # print("1 ", temp_path)
                        temp_items_seen = items_seen[paths.index(
                            old_path)].copy()

                        # -- we need to gatekeep to make sure that we are not exploring something we have already solved:
                        for y in range(len(_set)):
                            # -- for each item in the Cartesian product...

                            # if the input is already explore or the candidate fu of the input is already in the path
                            if inputs_evaluated[y] in temp_items_seen or _set[y] in temp_path:
                                # ... check if the object for the candidate unit already was solved:
                                # -- if the input object has already been seen, then no need to try and add a functional unit
                                # 	to the path that solves it again:
                                pass
                            else:
                                # searchNodes[inputs_evaluated[y]].print_functions[hierarchy_level-1]()
                                # -- we note if changes were made such that we will
                                # 	override the old paths list with new one:
                                changes = True

                                # -- append changes to the path and items seen lists:
                                temp_path.append(_set[y])
                                # print("2 ", temp_path)
                                temp_items_seen.add(inputs_evaluated[y])

                                candidates_for_stack.add(_set[y])
                                # tree_stack.append(_set[y])
                            # endif
                        # endfor

                        # print(temp_path)
                        # print(temp_items_seen)

                        new_paths.append(temp_path)
                        # print(temp_path)
                        # input()
                        new_items_seen[len(new_paths)-1] = temp_items_seen
                    # endfor
                else:
                    new_paths.append(old_path)
                    new_items_seen[len(new_paths) -
                                   1] = items_seen[paths.index(old_path)]

                # endif

            # endfor

            # input(len(new_paths) == len(new_items_seen))

            if changes:
                # -- we override the list of paths with the new set as well as the items seen for each path:
                paths = new_paths
                # print(len(paths))
                # paths = set([frozenset(x) for x in paths])
                # paths = [list(x) for x in paths]
                paths = list(k for k, _ in IT.groupby(paths))
                items_seen = new_items_seen

                # -- we only add certain elements to the tree stack if we need to further explore
                # 	(i.e. we added new things to paths)
                for C in candidates_for_stack:
                    tree_stack.append(C)

        # remove duplicate path
        # paths.sort()
        paths = list(k for k, _ in IT.groupby(paths))

        for P in paths:
            print("ss", P)

            # print(P)
            solutions.append(P)

        # print(len(solutions))

        # end_time = time.time()

        # print('   -- Time taken to explore root #' + str(root_nodes.index(_root)
        #                                                  ) + ' : ' + (str(end_time - start_time)) + ' s..')
    solutions = list(k for k, _ in IT.groupby(solutions))
    for S in solutions:
        # -- everything will be saved as reverse order, so switch it around.
        S.reverse()

        # -- save all task trees found by algorithm to this list:
        task_tree = [foon_functional_units[FU] for FU in S]
        all_path_trees.append(task_tree)

    return solutions, all_path_trees
# -----------------------------------------------------------------------------------------------------------------------------#


def save_paths(goal_id, all_paths):
    output_dir = "retrieved_tree/" + str(goal_id)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    for path in all_paths:
        task_tree = []
        for FU in path:
            task_tree.append(FU.get_FU_as_json())

        json.dump(task_tree, open(os.path.join(
            output_dir, str(all_paths.index(path)) + ".json"), "w"), indent=4)
# -----------------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":

    foon_functional_units, foon_object_nodes, foon_object_to_FU_map = read_universal_foon()

    print("STARTING SEARCH")
    goal_id = find_goal_id(GOAL_NODE)
    _, all_paths = search_all_path(goal_id)
    save_paths(goal_id, all_paths)
