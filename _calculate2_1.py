
import _Node
import _processing
import heapq

#### a very messy and single purpose calculation
#### takes a tower strucutre starting at a MasterNode
##### will print out the efficiency of the tower for 2 paths
TOTAlLIMIt = 7
MInLIMIt = 2
MAxLIMIt = 5
UPGRADePATHs = 2

def mainCalculate(tower):   


    efficientChoiceList = [] ## list of efficient choices, one for each path in the tower, are linked lists and use .attach
    ## aka our return data
    
    choiceNodes = [] ## list of nodes used for choice making, one for each path, points next to the upgrade that should be as option
    ###### choiceNodes should have a depth variable

    models = [] ## list of models created by each efficient choices, one for each path

    ## initialize all choice lists with the placement tower
    ## initialize all choice nodes to the head of each path chain
    ## initialize models, dummy nodes in correct amount

    for i in range(len(tower.path) - 1):  ### another instance of slicing the 0 index !!!!
        efficientChoiceList.append(_Node.LinkedDataList())
        # initialize after loop
        
        choiceNodes.append( _Node.Node( f"choice{i}", {"depth":1, "lock": None}  ) )
        #choiceNodes[i].next = tower.path[(i+1)].head ### another slice related patch !!!!

        models.append(_Node.Node("dummy"))
        efficientChoiceList[i].attach(tower.name, tower.data)
        ## also put the efficiency
        insertEfficiency( efficientChoiceList[i].head)


    for currentList in range(len(efficientChoiceList)):
        lockedTo = None
        #reset depths
        for i in range(len(choiceNodes)): # reset choices each list
            choiceNodes[i].next = tower.path[(i+1)].head # !!!!
            choiceNodes[i].data["depth"] = 1

        while efficientChoiceList[currentList].depth < 8: ## hard code upgrade limit !!!
            best_index = None
            heap=[]
            for i in range(len(models)):
                if choiceNodes[i].next == None: # if there are no more upgrades
                    continue

                models[i] = _Node.Node(choiceNodes[i].next.name, ( createUpgradedTowerData(efficientChoiceList[currentList].tail.data, choiceNodes[i].next.data ) ) )
                insertEfficiency(models[i])
                heap.append( (models[i].data["EfficiencyCost"], i) )
            heapq.heapify(heap)
            bestModel = heapq.heappop(heap)
            best_index = bestModel[1] ## which "i" path did win

            # set the lock when a new upgrade 3 is hit, locked list or old upgrade discarded

            while best_index != -1:
                
                if choiceNodes[best_index].data["depth"] == 3 and lockedTo == None and choiceNodes[best_index].data["lock"] == None:  
                    choiceNodes[best_index].data["lock"] = currentList
                    lockedTo = best_index

                if choiceNodes[best_index].data["depth"] < 3: # if insignificant
                    efficientChoiceList[currentList].attach(models[best_index].name, models[best_index].data)
                    choiceNodes[best_index].next = choiceNodes[best_index].next.next
                    choiceNodes[best_index].data["depth"] += 1
                    best_index = -1

                elif lockedTo == best_index and choiceNodes[best_index].data["lock"] == currentList: # upgrades must match to list and list much match to upgrades
                    efficientChoiceList[currentList].attach(models[best_index].name, models[best_index].data)
                    choiceNodes[best_index].next = choiceNodes[best_index].next.next
                    choiceNodes[best_index].data["depth"] += 1
                    best_index = -1

                else: # we successfuly rejected to upgrade
                    #get a new upgrade
                    if not heap:
                        best_index = -1
                    else:
                        bestModel = heapq.heappop(heap)
                        best_index = bestModel[1]    
    
    ############################## manual print in calc i am so lazy rn sry ;( ########################
    for i in range(len(efficientChoiceList)):
        print(f"     Path {i+1}")
        for node in efficientChoiceList[i]:
            print(f"{node.name}: {node.data['EfficiencyCost']} , {node.data['DMG']}")
            if node.data.get("DPS") != None:
                print(f"    DPS: {node.data['DPS']}")
    
######################## end of main #################


def insertEfficiency(node): 
    if "Burst" in node.data.keys() and node.data["Burst"] > 1:
        node.data["EfficiencyCost"] = node.data["Cost"] / ( (node.data["DMG"] * node.data["Burst"]) / (node.data["Reload"] + node.data["Burst"] * 0.1 ) )
        node.data["DPS"] = ( (node.data["DMG"] * node.data["Burst"]) / (node.data["Reload"] + node.data["Burst"] * 0.1 ) )
        #print(node.name, node.data["Cost"], node.data["DMG"], node.data["Burst"] , node.data["Reload"])
    else:
        node.data["EfficiencyCost"] = node.data["Cost"] / ( (node.data["DMG"]) / node.data["Reload"] )


def createUpgradedTowerData( entryData: dict, upgradeData: dict ):
    
    modelData = {}

    shared_keys = set(entryData.keys()) | set(upgradeData.keys())
    for key in shared_keys:
        delta_key = f"delta{key}" # explicitly refer to the delta of the base key

        if (key == "tags") or ("delta" in key): # ignore tags or delta values, avoids "deltadelta"
            continue
        else:
            fallback = {  # set fallback values if a key doesnt exist
                "Reload": 99, # special case
                "Burst": 1 }.get(key, 0) # get special case or usually nothing means 0
            modelData[key] = entryData.get(key, fallback) + upgradeData.get(delta_key, 0)

        ## bottom are overwrites to logic very lazy needs cleanup!!!
        if modelData.get("Reload") and ("Set Reload" in upgradeData.get("tags", [])):         
            modelData["Reload"] = upgradeData["Reload"]

        if modelData.get("Reload") != None and modelData["Reload"] < 0:
            modelData["Reload"] = entryData["Reload"]

    return modelData


'''
central data structure for calculator rules
holds static variables related to upgrade tree limits
    and choice nodes
'''

class choiceNode(): ## created by the choice controller only
    def __init__(self, node):
        # persistent memory
        self._1stupgrade = node
        self.commited = False
        # in-iteration memory
        self.next = self._1stupgrade
        self.locked = False
        self.level = 1

    def getUpgrade(self):
        return self.next
    
    def setNextUpgrade(self):
        if self.next.next == None or self.next.next.name == "nullNode":
            self.next = _Node.Node("nullNode", {})
        else:
            self.next = self.next.next
            self.depth += 1
    
    def reset(self):
        self.locked = False
        self.next = self._1stupgrade
        self.level = 1
            
            
class choiceController:
    def __init__(self, totalLimit, maxLimit, minLimit, choicePaths):
        self.totalLimit = totalLimit
        self.maxLimit = maxLimit
        self.minLimit = minLimit

        self.Locked = False
        self.UpgradePath = choicePaths
        self.choices = [] # choice nodes for all linked list paths

        for path in self.UpgradePath:
            self.choices.append(choiceNode(path.head))

    def resetIteration(self):
        self.Locked = False
        # reset each choice state
        for choice in self.choices:
            choice.reset()

    
    def pickValidChoices(self):
        validChoices = []

        for choice in self.choices:
            if choice.level < self.minLimit: ## rule, all minimals are valid
                validChoices.append(choice)
                continue
            if choice.level == (self.minLimit + 1) and choice.commited == False and self.Locked == False: # rule, commitment level valid if never commited
                validChoices.append(choice)
                continue
            if choice.level > self.minLimit and choice.locked == True and self.Locked == True: # rule, all over minimals valid if locked this iteration
                validChoices.append(choice)
                continue            

        if len(validChoices) == 0:
            return None
        if len(validChoices) == 1:
            return validChoices[0]
        else:
            return validChoices
        
    def pickedChoice(self, choice):
        if choice in self.choices:
            choice.setNextUpgrade()
            choice.level += 1
            if choice.level > self.minLimit:
                choice.locked = True
                choice.commited = True
                self.Locked = True

    

"""
WRITE SOME ASSERTS MY GUY

USE SOME PDB
PDB.SETTRACE MY GUY

"""