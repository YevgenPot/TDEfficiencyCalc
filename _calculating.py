import _Node
import _processing


def mainCalculate(tower_list):
    ### this calculator assumes multiple paths
    tower = tower_list

    #test prints
    ##print(tower[0].path[1].head.next.next.data.keys())
    
    for i in range(len(tower)): ## index through the tower list
        #put the tower data into a new list
        
        towerNode = _Node.MasterNode(tower[i].name, tower[i].data)
        upgradeslist= []




        trackerNode = _Node.MasterNode("tracker", {})
        for each path in tower
            trackerNode.path[i] = potentialNode
            trackerNode.data[f"depth{i}"] = 1
        
        

        # evaulate an augmented tower for each upgrade path
        # evaluate the next efficient augemnted tower

        currentBuild
        for each path
            place all options in list
            calc efficiency
            store efficiency







        # track the winners and losers

        # keep evaluating
        # next choices should be the loser and the winner.next

        # until the 3rd upgrade of any path is about to be chosen
        #### aka if winner is the 3rd upgrade of any path
        #TWO TASKS
        # 1. make the winning choice, evaulate the augment tower of the winning path, until no more upgrades can be made
        # 2. force the losing choice, evaulate the augment tower of the losing path, 
        ##### mark if it was forced, until the 3rd upgrade of the losing path is chosen
        ########## evaluate until no more upgrades can be made





########################## end of main #################################


### calc
### we have a collection of upgrades
### for example, 3 from each upgrade path, in fact the first 3
### after 3 upgrades, choice is lost and simple efficiency calculations
#### find when a 3rd gets chosen -> continue finding cost efficiencies
###  also
### make new sequence of calculations
### instead of the winning 3rd upgrade, force it to make the inefficenct choice, mark as Forced
#### for every remaining upgrade in the loser path, keep making the loser path choice, checking if subsequent choices are forced
##### until the 3rd upgrade of the loser path is chosen -> continue finding cost efficiencies
# ai interpretation of this abstract plan is this looks like: bounded search tree traversal with decision recording


'''
get a tower is the masternode is the index in the list
initialize the tower is the master node data

'''


def evaluateAugmentedTower(entryData: dict, exitData: dict): # works on the node.data
    augmentNode = _Node.Node(exitData.name)
    for key in entryData.keys():
        if key == "tags":
            pass
        else:
            delta_key = f"delta{key}"
            augmentNode.data[key] = entryData[key] + exitData[delta_key]

