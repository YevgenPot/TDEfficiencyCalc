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

    choiceControllerObj = choiceController(TOTAlLIMIt, MAxLIMIt, MInLIMIt, tower.path[1:] ) ## !!!! manual slicing

    greedySequence = []
    models = []
    heap = []
    for i in range(len(tower.path) - 1):  ### another instance of slicing the 0 index !!!!
        greedySequence.append(_Node.LinkedDataList())
        greedySequence[i].attach(tower.name, tower.data)
        insertEfficiency( greedySequence[i].head.data) # !!!
        models.append(_Node.Node("dummy"))



    for currentSequence in greedySequence: ## fill all lists

        while choiceControllerObj.pickValidChoices() != None:
            best_index = None
            validChoicePointers = choiceControllerObj.pickValidChoices()
            if len(validChoicePointers) == 1:
            # only one valid choice found using ruleset
            # simply model it and add
                models[0] = _Node.Node( 0 , ( createUpgradedTowerData(currentSequence.tail.data, validChoicePointers[0].next.data ) ) )

                currentSequence.attach( validChoicePointers[0].next.name , models[0].data) # !!!
                choiceControllerObj.pickedChoice( validChoicePointers[0] )
            else:
                for i, choice in enumerate( validChoicePointers ) :
                    models[i] = _Node.Node( i , ( createUpgradedTowerData(currentSequence.tail.data, choice.next.data) ) )
                    heap.append( (models[i].data["EfficiencyCost"], i) )
                heapq.heapify(heap) ### heap no longer optimal, since only 1 best is popped per iteration
                bestModel = heapq.heappop(heap)
                best_index = bestModel[1] ## which "i" path did win
                
                currentSequence.attach( validChoicePointers[best_index].next.name, models[best_index].data) ## !!!
                choiceControllerObj.pickedChoice( validChoicePointers[best_index] )
                heap.clear()
        choiceControllerObj.resetIteration()

    return greedySequence
######################## end of main #################

def insertEfficiency(dataDict): 
    if "Burst" in dataDict.keys() and dataDict["Burst"] > 1:
        dataDict["EfficiencyCost"] = dataDict["Cost"] / ( (dataDict["DMG"] * dataDict["Burst"]) / (dataDict["Reload"] + dataDict["Burst"] * 0.1 ) )
        dataDict["DPS"] = ( (dataDict["DMG"] * dataDict["Burst"]) / (dataDict["Reload"] + dataDict["Burst"] * 0.1 ) )
        #print(node.name, dataDict["Cost"], dataDict["DMG"], dataDict["Burst"] , dataDict["Reload"])
    else:
        dataDict["EfficiencyCost"] = dataDict["Cost"] / ( (dataDict["DMG"]) / dataDict["Reload"] )


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

    
    insertEfficiency(modelData)
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
        self.level += 1
        if self.next.next == None or self.next.next.name == "nullNode":
            self.next = _Node.Node("nullNode", {})
        else:
            self.next = self.next.next
    
    def reset(self):
        self.next = self._1stupgrade
        self.locked = False
        self.level = 1
            
            
class choiceController:
    def __init__(self, totalLimit, MaxLimit, MinLimit, choicePaths):
        self.totalLimit = totalLimit
        self.maxLimit = MaxLimit
        self.minLimit = MinLimit

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
            #print( f'choice level: {choice.level}, locked: {choice.locked}, commited: {choice.commited}' )
            if choice.level <= self.minLimit: ## rule, all minimals are valid
                validChoices.append(choice)
                continue
            if choice.level == (self.minLimit + 1) and choice.commited == False and self.Locked == False: # rule, commitment level valid if never commited
                validChoices.append(choice)
                continue
            if choice.level <= self.maxLimit and choice.locked == True and self.Locked == True: # rule, all over minimals valid if locked this iteration
                validChoices.append(choice)
                continue      
    

        if len(validChoices) == 0:
            return None
        else:
            return validChoices
        
    def pickedChoice(self, choice):
        if choice in self.choices:
            if choice.level == (self.minLimit + 1):
                choice.locked = True
                choice.commited = True
                self.Locked = True
            
            choice.setNextUpgrade()
