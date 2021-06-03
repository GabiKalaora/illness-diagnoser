import random
import itertools


class Node:
    """
    class Node defines the tree with true as
    positive_child and False as negative_child
    """

    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child


class Record:
    """
    class Record holds the fields, illness = string of a name of a illness,
     symptoms = list of strings with symptoms
     """

    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    """
    this function gets a file with illness and symptoms attached
    to that illness
    """

    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """
    class Diagnoser gets a tree and acts on it with methods. as will be
    explained in coming methods in Diagnoser class
    """

    def __init__(self, root):
        self.root = root

    def diagnose_helper(self, symptoms, root):
        """
        this method helps diagnose method gets list of symptoms and finds
        illness that fits all symptoms according to given decision tree
        """

        if root.positive_child is None:
            return root.data
        if root.data in symptoms:
            return self.diagnose_helper(symptoms, root.positive_child)
        else:
            return self.diagnose_helper(symptoms, root.negative_child)

    def diagnose(self, symptoms):
        """
        this method gets list of symptoms and finds illness that fits all
         symptoms according to given decision tree by using helper diagnose
         """

        return self.diagnose_helper(symptoms, self.root)

    def calculate_success_rate(self, records):
        """
        this method checks rate of success of records to find illness
        according to list of symptom by using diagnose method to
        find right illness
        """

        score = 0
        for record in records:
            if self.diagnose(record.symptoms) == record.illness:
                score += 1
        return score / len(records)

    def all_illnesses_helper(self, root, lst):
        """
        this method is helper to all illnesses method, this method runs
        through all tree and returns all illnesses in tree
        """

        if root.positive_child is None:
            lst.append(root.data)
            return lst
        self.all_illnesses_helper(root.positive_child, lst)
        self.all_illnesses_helper(root.negative_child, lst)
        return lst

    def all_illnesses(self):
        """
        this method gets lst of all illnesses from helper and return a
        sorted list according to appearances of illness in tree more
        appearances first in list and so on
        """

        lst_of_illnesses = []
        lst = self.all_illnesses_helper(self.root, [])
        lst = sorted(lst, key=lst.count, reverse=True)
        [lst_of_illnesses.append(item) for item in lst if
         item not in lst_of_illnesses]
        return lst_of_illnesses

    def paths_to_illness_helper(self, illness, root, path, path_of_illness):
        """
        this method is helper to path of illness method gets an illness and
        runs on tree and finds all paths to that illness
        """

        if root.positive_child is None:
            if root.data == illness:
                path_of_illness.append(path[::])
                if path:
                    del path[-1]
            else:
                if path:
                    del path[-1]
            return path_of_illness

        path.append(True)
        self.paths_to_illness_helper(illness, root.positive_child, path,
                                     path_of_illness)
        if root.data == self.root.data:
            path.clear()
        path.append(False)
        self.paths_to_illness_helper(illness, root.negative_child, path,
                                     path_of_illness)
        if path:
            del path[-1]
        return path_of_illness

    def paths_to_illness(self, illness):
        """
        this method  gets an illness and runs on tree and
        finds all paths to that illness
        """

        return self.paths_to_illness_helper(illness, self.root, [], [])


def all_paths_in_tree(nodes_lst):
    """
    This function finds all the possible paths from a given list of nodes
    not included the leaves of tree
    """
    if not nodes_lst:
        return [[]]
    lst_of_paths = all_paths_in_tree(nodes_lst[1:])
    return lst_of_paths + [[nodes_lst[0]] + rest_of_lst for rest_of_lst in
                           lst_of_paths]


def get_all_illnesses(tree, all_illnesses):
    """
    This function runs recursively on a tree and adds all the leaves(illnesses)
    in it to a all leaves list
    """
    if tree.positive_child:
        get_all_illnesses(tree.negative_child, all_illnesses)
        get_all_illnesses(tree.positive_child, all_illnesses)
    else:
        all_illnesses.append(tree)


def get_illness_from_illnesses(records, tree):
    """
    This function replaces list of many illnesses from list we got from previous
    func function with a single illness that is most common illness in list """

    all_illnesses_possible = []
    for record in records:
        all_illnesses_possible.append(record.illness)

    all_illnesses = []
    get_all_illnesses(tree, all_illnesses)
    for illness in all_illnesses:
        if not illness.data:
            illness.data = random.choice(list(set(all_illnesses_possible)))
        else:
            count = {}
            for item in list(illness.data):
                count[item] = list(illness.data).count(item)
            illness.data = max(count, key=count.get)


def find_all_illness(records, symptoms, tree):
    """
    This function matches an illnesses to each leaf, according to appearances
    of each path and each symptom list from each record by finding all suitable
    illnesses and returning the one illness bt using get illness from illnesses
    """

    all_paths = all_paths_in_tree(symptoms)
    for single_path in all_paths:
        for record in records:
            flag = True
            for path in single_path:
                if path not in record.symptoms:
                    flag = False
            for symptom in symptoms:
                if symptom not in single_path and symptom in record.symptoms:
                    flag = False
            if flag:
                empty_illness_lst = Diagnoser(tree).diagnose(single_path)
                empty_illness_lst.append(record.illness)
    get_illness_from_illnesses(records, tree)


def build_tree_helper(records, symptoms, symptom_index, root):
    """
    This function builds a tree all the leaves are empty strings by running by 
    length of num of symptoms and adds positive_child and negative_child as needed
    """

    if symptom_index == len(symptoms):
        return
    else:
        root.data = symptoms[symptom_index]
        root.positive_child = Node([])
        root.negative_child = Node([])
        build_tree_helper(records, symptoms, symptom_index + 1,
                          root.positive_child)
        build_tree_helper(records, symptoms, symptom_index + 1,
                          root.negative_child)


def build_tree(records, symptoms):
    """
    This function places parameters for build_tree_helper function.
    """

    symptom_index = 0
    root = Node([])
    build_tree_helper(records, symptoms, symptom_index, root)
    find_all_illness(records, symptoms, root)
    return root


def optimal_tree(records, symptoms, depth):
    """
    This function returns a single tree with highest success rate from all
    possible trees that we can create with all the combinations that fits
    symptoms by using calculate_success_rate method from class Diagnoser
    """

    all_trees = {}
    for combination in itertools.combinations(symptoms, depth):
        tree = build_tree(records, combination)
        tree_success_rate = Diagnoser(tree).calculate_success_rate(records)
        all_trees[tree_success_rate] = tree
    tree_optimal = max(all_trees)
    return all_trees[tree_optimal]


if __name__ == "__main__":
    	# Manually build a simple tree.
	#                cough
	#          Yes /       \ No
	#        fever           healthy
	#   Yes /     \ No
	# covid-19   cold
	
	flu_leaf = Node("covid-19", None, None)
	cold_leaf = Node("cold", None, None)
	inner_vertex = Node("fever", flu_leaf, cold_leaf)
	healthy_leaf = Node("healthy", None, None)
	root = Node("cough", inner_vertex, healthy_leaf)
	
	diagnoser = Diagnoser(root)
	
	# basic of the basics test
	diagnosis = diagnoser.diagnose(["cough"])
	if diagnosis == "cold":
		print("Test passed")
	else:
		print("Test failed. Should have printed cold, printed: ", diagnosis)
