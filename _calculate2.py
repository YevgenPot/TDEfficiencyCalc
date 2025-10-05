
import _Node
import _processing

#### a very messy and single purpose calculation
#### takes a tower strucutre starting at a MasterNode
##### will print out the efficiency of the tower for 2 paths

def mainCalculate(tower):   


    efficientChoiceList = [] ## list of efficient choices, one for each path in the tower, are linked lists and use .attach
    choiceNodes = [] ## list of nodes used for choice making, one for each path, points next to the upgrade that should be as option
    ###### choiceNodes should have a depth variable
    models = [] ## list of models created by each efficient choices, one for each path

    ## initialize all choice lists with the placement tower
    ## initialize all choice nodes to the head of each path chain
    ## initialize models, dummy nodes in correct amount

    for i in range(len(tower.path) - 1):  ### another instance of slicing the 0 index !!!!
        efficientChoiceList.append(_Node.LinkedDataList())
        # initialize after loop
        
        choiceNodes.append( _Node.Node( f"choice{i}", {"depth":1}  ) )
        choiceNodes[i].next = tower.path[(i+1)].head ### another slice related patch !!!!

        models.append(_Node.Node("dummy"))
    efficientChoiceList[0].attach(tower.name, tower.data) # initialize the fisrt best list
    ## also put the efficiency
    insertEfficiency( efficientChoiceList[0].head)

    currentList = 0
    while currentList < len(efficientChoiceList) : 
        best_score = None
        best_index = None
        for i in range(len(models)):
            if choiceNodes[i].data["depth"] == 3: # the choice's depth is 3, it gives up trying to win
                continue
            models[i] = _Node.Node(choiceNodes[i].next.name, ( createUpgradedTowerData(efficientChoiceList[currentList].tail.data, choiceNodes[i].next.data ) ) ) ## this is wrong!!!!
            insertEfficiency(models[i])

            if best_score == None:
                best_score = models[i].data["EfficiencyCost"]
                best_index = i
            elif models[i].data["EfficiencyCost"] < best_score:
                best_score = models[i].data["EfficiencyCost"]
                best_index = i

        efficientChoiceList[currentList].attach(models[best_index].name, models[best_index].data)
        choiceNodes[best_index].next = choiceNodes[best_index].next.next
        choiceNodes[best_index].data["depth"] += 1
        if choiceNodes[best_index].data["depth"] == 3: # the choice's depth is 3, it gives up trying to win
            currentList += 1 # now we start filling the 2nd best efficient list
            if currentList < len(efficientChoiceList):
                efficientChoiceList[currentList].attach(models[best_index].name, models[best_index].data) # initialize the next best efficient list with the current best

    
    
    for i in range(len(choiceNodes)):
        while choiceNodes[i].data["depth"] <=5 :
            models[i] = _Node.Node(choiceNodes[i].next.name, ( createUpgradedTowerData(efficientChoiceList[i].tail.data, choiceNodes[i].next.data ) ) ) 
            insertEfficiency(models[i])
            efficientChoiceList[i].attach(models[i].name, models[i].data)
            choiceNodes[i].next = choiceNodes[i].next.next
            choiceNodes[i].data["depth"] += 1 
            
    
    
    ############################## manual print in calc i am so lazy rn sry ;( ########################
    for i in range(len(efficientChoiceList)):
        print(f"     Path {i+1}")
        for node in efficientChoiceList[i]:
            print(f"{node.name}: {node.data['EfficiencyCost']}")
######################## end of main #################


def insertEfficiency(node):
    if "Burst" in node.data.keys():
        node.data["EfficiencyCost"] = node.data["Cost"] / ( (node.data["DMG"] * node.data["Burst"]) / node.data["Reload"] )
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
    return modelData
