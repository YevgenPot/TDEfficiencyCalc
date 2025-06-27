import numpy
import math
import _inputModule

def mainProcess():

    towers_data = _inputModule.mainInput()

    #for key, value in dictionary.items():
    # then that value is actually a value_dictionary
    # so then
    #  for key1, value1 in value_dictionary.keys():


    tower_list = []

    for tower_name, levels_data in towers_data.items():
        #tower_obj = twoPathTower(tower_name) # create new tower
        linkList = LinkedUpgradeList()
        linkList.name = tower_name
        tower_list.append(linkList) # add to list

        for upgradeState, parameters_data in levels_data.items():
            linkList.attach(upgradeState, parameters_data)

            #for parameter, value in parameters_data.items():

            


    #end of for loop  

    for i in range(len(tower_list)):
        recursiveCost(tower_list[i].tail1)
        recursiveCost(tower_list[i].tail2)

        recursiveStats(tower_list[i].tail1)
        recursiveStats(tower_list[i].tail2)

        print("  ", tower_list[i].name)
        generateCostEfficiency(tower_list[i])

    


    
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

    ## does not bake in the 3 and 5 rule
    ## 3 - only one path can go past 3
    ## 5 - no path can go past 5
    """

    efficienyList = []
    efficienyList.append(linkedList.head)
    insertEfficiency(efficienyList[0])
    print("placement", linkedList.head.upg_data["EfficiencyCost"])
    function(linkedList.head, linkedList.head.path1, linkedList.head.path2, efficienyList,0,0)

    #for node in efficienyList:
    #    print(node.name, node.upg_data["EfficiencyCost"])


def function(initialNode, choice1Node, choice2Node, efficiencyList, path1depth, path2depth):

    if choice1Node == None or choice2Node == None:
        return
    model1 = makeModelNodeWith(initialNode, choice1Node)
    model2 = makeModelNodeWith(initialNode, choice2Node)

    insertEfficiency(model1)
    insertEfficiency(model2)

    if path2depth > 2 and path1depth == 2:
        model1.upg_data["EfficiencyCost"] = 9999
    if path1depth > 2 and path2depth == 2:
        model2.upg_data["EfficiencyCost"] = 9999
        
    if model1.upg_data["EfficiencyCost"] < model2.upg_data["EfficiencyCost"]:
        print(model1.name, model1.upg_data["EfficiencyCost"])
        efficiencyList.append(model1)
        path1depth += 1
        initialNode = model1
        if choice1Node.next == None:
            return
        choice1Node = choice1Node.next

        function(initialNode, choice1Node, choice2Node, efficiencyList, path1depth, path2depth)
    else:
        print(model2.name, model2.upg_data["EfficiencyCost"])
        efficiencyList.append(model2)
        path2depth += 1
        initialNode = model2
        if choice2Node.next == None:
            return
        choice2Node = choice2Node.next
        function(initialNode, choice1Node, choice2Node, efficiencyList, path1depth, path2depth)

def makeModelNodeWith(node1, node2):
    model = Node(node2.name, {})
    model.upg_data["Cost"] = node1.upg_data["Cost"] + node2.upg_data["deltaCost"]
    model.upg_data["DMG"] = node1.upg_data["DMG"] + node2.upg_data["deltaDMG"]
    model.upg_data["Reload"] = node1.upg_data["Reload"] + node2.upg_data["deltaReload"]
    if node2.upg_data.get("tags") != None:
        if "[Set Reload]" in node2.upg_data.get("tags"):
            model.upg_data["Reload"] = node2.upg_data["Reload"]
    model.upg_data["Range"] = node1.upg_data["Range"] + node2.upg_data["deltaRange"]
    if "Burst" in node1.upg_data.keys():
        model.upg_data["Burst"] = node1.upg_data["Burst"] + node2.upg_data["deltaBurst"]
    return model

def insertEfficiency(node):
    if "Burst" in node.upg_data.keys():
        node.upg_data["EfficiencyCost"] = node.upg_data["Cost"] / ( (node.upg_data["DMG"] * node.upg_data["Burst"]) / node.upg_data["Reload"] )
        #print(node.name, node.upg_data["Cost"], node.upg_data["DMG"], node.upg_data["Burst"] , node.upg_data["Reload"])
    else:
        node.upg_data["EfficiencyCost"] = node.upg_data["Cost"] / ( (node.upg_data["DMG"]) / node.upg_data["Reload"] )

    ##if node.upg_data["EfficiencyCost"] < 0:
        #print( node.upg_data["Cost"], node.upg_data["DMG"], node.upg_data["Reload"] )
        #print(node.name, node.upg_data["Cost"], node.upg_data["DMG"], node.upg_data["Reload"])

def upgradeLoser(node1, node2, efficiencyList):
    upgrade = makeModelNodeWith(node1, node2)
    insertEfficiency(upgrade)
    efficiencyList.append(upgrade)
    
    return upgrade

#############
            
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