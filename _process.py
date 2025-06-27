import numpy
import math
import _inputModule

def mainProcess():

    towers_data = _inputModule.mainInput()

    #for key, value in dictionary.items():
    # then that value is actually a value_dictionary
    # so then
    #  for key1, value1 in value_dictionary.keys():
    """
    for tower_name, levels_data in towers_data.items():
        print(f"Tower: {tower_name}")
        for upgradeState, parameters_data in levels_data.items():
            print(f"Upgrade State: {upgradeState}") # eg placement
            for parameter, value in parameters_data.items():
                print(f"{parameter}: {value}") # eg Cost
                if value == 7250:
                    print("RIGHT HERE")


    if parameters_data.get("tags") != None:
                print(parameters_data.get("tags")[0])
                if "[Air Target]" in parameters_data.get("tags"):
                    print("!!!!!!!!!!!!!!!!!")
    """


    tower_list = []
    
    linkList = LinkedUpgradeList()

    for tower_name, levels_data in towers_data.items():
        #tower_obj = twoPathTower(tower_name) # create new tower
        #tower_list.append(tower_obj) # add to list

        holder = "nil" # temporary holder

        for upgradeState, parameters_data in levels_data.items():
            linkList.attach(upgradeState, parameters_data)

            #for parameter, value in parameters_data.items():

            


    #end of for loop  
    recursiveCost(linkList.tail1)
    recursiveCost(linkList.tail2)

    recursiveStats(linkList.tail1)
    recursiveStats(linkList.tail2)


    generateCostEfficiency(linkList)

    


    
###################################### end of main


def recursiveCost(node):
    if node.name == "placement":
        totalCost = node.upg_data["Cost"]
        return totalCost
    else:
        totalCost = recursiveCost(node.prev) + node.upg_data["deltaCost"]
        node.upg_data["Cost"] = totalCost
        return totalCost


##########
def recursiveStats(node):
    if node.name == "placement":
        return node.upg_data
    else:
        insertDeltaParams(node.upg_data, recursiveStats(node.prev))
        return node.upg_data
    
def insertDeltaParams(dict2: dict, dict1: dict):
    shared_keys = set(dict1.keys()) | set(dict2.keys())
    for key in shared_keys:
        delta_key = f"delta{key}"
        delta_value = 0
        if key not in {"DMG", "Reload", "Range", "Burst"}:
            pass
        else:
            if key == "DMG":
                delta_value = dict2.get(key, 0) - dict1.get(key, 0)
            if key == "Reload":
                delta_value = dict2.get(key, 99) - dict1.get(key, 99)
            if key == "Range":
                delta_value = dict2.get(key, 0) - dict1.get(key, 0)
            if key == "Burst":
                delta_value = dict2.get(key, 1) - dict1.get(key, 1)
            dict2[delta_key] = delta_value


#####################

def generateCostEfficiency(linkedList):
    """
    have initial state
    set up choices
    find choice winner

    inital state is winner
    use loser to set up choices

    find choice winner

    until initial state is None
    """

    efficienyList = []
    efficienyList.append(linkedList.head.upg_data)
    function(linkedList.head, linkedList.head.path1, linkedList.head.path2, efficienyList)
    '''
    initialNode = linkedList.head

    choice1Node = linkedList.head.path1
    choice2Node = linkedList.head.path2

    model1 = setModelWith(initialNode, choice1Node)
    model2 = setModelWith(initialNode, choice2Node)

    if model1["EfficiencyCost"] < model2["EfficiencyCost"]:
        efficienyList.append(model1)
        choice1Node = linkedList.head.path1.next
    else:
        efficienyList.append(model2)
        choice2Node = linkedList.head.path2.next

    while winnerNode.next != None:

        initialNode = winnerNode
        initialNode.upg_data["CostEfficiency"] = calcefficiency(initialNode)
        efficienyList.simpleAttach(initialNode.name, initialNode.upg_data)

        winnerNode, loserNode = choiceWinner(initialNode, winnerNode.next, loserNode)
    '''
    for node in efficienyList:
        print(node.name, node.upg_data["CostEfficiency"])


def function(initialNode, choice1Node, choice2Node, efficiencyList):
    model1 = setModelWith(initialNode, choice1Node)
    model2 = setModelWith(initialNode, choice2Node)

    if model1["EfficiencyCost"] < model2["EfficiencyCost"]:
        efficiencyList.append(setModelWith(model1, efficiencyList[0]))
        initialNode = choice1Node
        choice1Node = choice1Node.next
        function(initialNode, choice1Node, choice2Node, efficiencyList)
    else:
        efficiencyList.append(setModelWith(model2, efficiencyList[0]))
        initialNode = choice2Node
        choice2Node = choice2Node.next
        function(initialNode, choice1Node, choice2Node, efficiencyList)



def setModelWith(node1, node2):
    print(node1.name, node2.name)
    model = {}
    model["name"] = node2.name
    model["Cost"] = node1.upg_data["Cost"] + node2.upg_data["deltaCost"]
    model["DMG"] = node1.upg_data["DMG"] + node2.upg_data["deltaDMG"]
    model["Reload"] = node1.upg_data["Reload"] + node2.upg_data["deltaReload"]
    model["Range"] = node1.upg_data["Range"] + node2.upg_data["deltaRange"]
    if "Burst" in node1.upg_data.keys():
        model["Burst"] = node1.upg_data["Burst"] + node2.upg_data["deltaBurst"]
        model["EfficiencyCost"] = model["Cost"] / ( (model["DMG"] * model["Burst"]) / model["Reload"] )
    else:
        model["EfficiencyCost"] = model["Cost"] / ( (model["DMG"]) / model["Reload"] )
    return model


#############

"""
class twoPathTower:
    def __init__(self, tower_name):
        self.tower_name = tower_name
        self.upgrades_data = {
            "placement": {},
            "path": {
                1: {
                     1: {},
                     2: {},
                     3: {},
                     4: {},
                     5: {}
                },
                2: {
                     1: {},
                     2: {},
                     3: {},
                     4: {},
                     5: {}
                }
            }
        }


    def insertData(self, upgradeState, params_data):
        self.upgrades_data[upgradeState] = params_data # add upgrade to pool
        if upgradeState == "placement":
            self.upgrades_data["placement"].update(params_data) # add upgrade to pool
        elif upgradeState.startswith("up1"):
                self.upgrades_data["path"]["1"][upgradeState].update(params_data) # add upgrade to pool
        elif upgradeState.startswith("up2"):
                self.upgrades_data["path"]["2"][upgradeState].update(params_data) # add upgrade to pool

    def insertDeltaParam(self, upgradeState, parameter):
        if upgradeState in self.upgrades_data["path"]["1"]:
            self.upgrades_data["path"]["1"][upgradeState]["delta" + parameter] = self.upgrades_data["path"]["1"][upgradeState]["level"]-1
            for

    def insertData1(self, upgradeState, params_data):
        if upgradeState == "placement":
            self.upgrades_data["placement"].update(params_data) # add upgrade to pool
"""
            
class Node:
    def __init__(self, name, data):
        self.name = name          # e.g., "placement", "up1-1"
        self.upg_data = data          # stat dictionary
        self.next = None          # pointer to next node
        self.prev = None          # (optional) for doubly linked
        self.path1 = None
        self.path2 = None   # only used for placement node

class LinkedUpgradeList:
    def __init__(self):
        self.head = None
        self.tail1 = None
        self.tail2 = None

    def attach(self, name, data):
        new_node = Node(name, data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            if not self.head.path1 and new_node.name.startswith("up1"):
                new_node.prev = self.head
                self.head.path1 = new_node
                new_node.next = None
                self.tail1 = new_node
            else:
                if new_node.name.startswith("up1"):
                    self.tail1.next = new_node
                    new_node.prev = self.tail1  # for doubly linked list support
                    self.tail1 = new_node

            if not self.head.path2 and new_node.name.startswith("up2"):
                new_node.prev = self.head
                self.head.path2 = new_node
                new_node.next = None
                self.tail2 = new_node
            else:
                if new_node.name.startswith("up2"):
                    self.tail2.next = new_node
                    new_node.prev = self.tail2  # for doubly linked list support
                    self.tail2 = new_node
        
    def simpleAttach(self, name, data):
        new_node = Node(name, data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail  # for doubly linked list support
            self.tail = new_node


    def __iter__(self):  ## careful to not iterate from head, as it would have no next
        current = self.head
        while current:
            yield current
            current = current.next

    def find(self, name): ## ditto above
        for node in self:
            if node.name == name:
                print(node.name)
                return node
        return None







if __name__ == "__main__":

    mainProcess()