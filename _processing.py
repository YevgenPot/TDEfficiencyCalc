'''
processing module
takes the dictionary strcture from _inputModule.py
and interprets the data

'''

import _inputModule
import _Node

def mainProcess(tower_data):

    #tower_data = _inputModule.mainInput() # replace with inputn parameter 
    tower_list = [] # list of all tower chains

    ############### giant loop to format data to linked nodes structure ##################

    ## looping through key towers, data dictionary of all upgrades
    for tower_name, levels_data in tower_data.items():
        placement_node = _Node.MasterNode(tower_name) # make the head node that will be the initial tower
        tower_list.append(placement_node) # the start of the tower chain
        ismultiPath = None

        # make the upgrade chains
        if any("-" in key for key in levels_data): # if the dash is detected, there are multiple upgrade paths, key is equivelant to below upgradeState
            ismultiPath = True
            temp = 0
            while True:
                temp += 1 # look at the next potential path
                s = f"up{temp}-" # create the upgrade path string
                if any(s in key for key in levels_data): # if the upgrade path prefix is found
                    tower_upgrades_list = _Node.LinkedDataList()
                    placement_node.attachPath(tower_upgrades_list) # append a new linked data list
                else:
                    break # stop when the next path doesnt exist
        else:
            ismultiPath = False
            tower_upgrades_list = _Node.LinkedDataList() # upgardes are single digit, only 1 upgrade path
            placement_node.attachPath(tower_upgrades_list)

        ## looping through key individual upgrade state, data dictionary of stats and info of each upgrade
        for upgradeState, parameters_data in levels_data.items():
            if upgradeState == "placement":
                placement_node.data = parameters_data # the placement tower and placement node
            else: # else the upgrade nodes need to be placed in chains
                if ismultiPath == True:
                    # multiple paths, place to appropriate path
                    index = int(upgradeState[2]) # what path the node goes to determined by the numerical char 1-9, so limit of 9 paths soft coded here!!!!
                    placement_node.path[index].attach(upgradeState, parameters_data)
                elif ismultiPath == False:
                    # single upgrade path, attach to the only path
                    placement_node.path[1].attach(upgradeState, parameters_data) # path[1] should be valid here
        
        for i in range(1, len(placement_node.path)): ## still for this current tower's master node
            # slice 0 for intuitive path picking, no path 0
            # should overwrite this behavior later !!!!
            placement_node.path[i].head.prev = placement_node ## all paths have been created, now link the chain to master node

    ## all the chains are made and stored in master nodes's paths
    ## all master nodes in tower_list

    ############# end of giant loop ###################

    ''' # print test of all elements
    for i in range(len(tower_list)):
        print( tower_list[i].path[2].head.prev.name, tower_list[i].path[1].head.name, tower_list[i].path[2].tail.name )
        '''

    ######################## data processing ######################
    ### fill in some key data that may not have been inserted during manual data input
    
    for i in range(len(tower_list)):
        for j in range(1, len(tower_list[i].path)): ## another instance of manual list slice !!!!
            recursiveStats(tower_list[i].path[j].tail)
    
    ''' # print test
    x=2
    print(  tower_list[x].path[1].head.prev.name, tower_list[x].path[1].tail.name, tower_list[x].path[1].tail.data["Cost"], tower_list[x].path[1].tail.data["DMG"] )
    '''

    return tower_list


################## end of main ####################


def recursiveStats(node):
    if type(node) == _Node.MasterNode:
        return node.data
    else:
        insertTotalCost( recursiveStats(node.prev), node.data ) ## I may or may not be using this data ????
        insertDeltaParams( recursiveStats(node.prev), node.data )
        return node.data
    
def insertDeltaParams(entryData: dict, exitData: dict): ## works directly on the node.data, and uses a node and its adjacent
    ## the output is the values that change the stats of entryData to exitData
    ## output to 2nd param node
    shared_keys = set(entryData.keys()) | set(entryData.keys()) 
    for key in shared_keys:

        ### calculate delta values of specific stats at each upgrade
        delta_key = f"delta{key}"
        delta_value = 0
        '''
        if key not in {"DMG", "Reload", "Range", "Burst"}: ## list of stats to turn to delta values
            pass
        else:
            if key == "DMG":
                delta_value = exitData.get(key, 0) - entryData.get(key, 0) 
            if key == "Reload":
                delta_value = exitData.get(key, 99) - entryData.get(key, 99) 
            if key == "Range":
                delta_value = exitData.get(key, 0) - entryData.get(key, 0)
            if key == "Burst":
                delta_value = exitData.get(key, 1) - entryData.get(key, 1)

            exitData[delta_key] = delta_value # writes new entry to data

        if (key == "tags") or ("delta" in key):
            continue
        elif key == "Reload":
                delta_value = exitData.get(key, 99) - entryData.get(key, 99) 
        elif key == "Burst":
                delta_value = exitData.get(key, 1) - entryData.get(key, 1)
        else:
            delta_value = exitData.get(key, 0) - entryData.get(key, 0)
        exitData[delta_key] = delta_value
        '''
        if (key == "tags") or ("delta" in key): # ignore tags or delta values
            continue
        else:
            fallback = {  # set fallback values if a key doesnt exist
                "Reload": 99, # special case
                "Burst": 1 }.get(key, 0) # get special case or usually nothing means 0
            delta_value = exitData.get(key, fallback) - entryData.get(key, fallback)
            exitData[delta_key] = delta_value


def insertTotalCost(entryData: dict, exitData: dict): 
    ## the output is the total cost of the exitData given that entryData has a cost and exitData has a deltaCost
    exitData["Cost"] = exitData["deltaCost"] + entryData["Cost"]



if __name__ == "__main__":
    mainProcess()



