import _inputModule
import _processing
import _calculate2_2
import _output

def main():
    towers_data = _inputModule.mainInput("entry.txt")
    towers_list = _processing.mainProcess(towers_data)


    linkedListsByName = {}
    for i, tower in enumerate(towers_list):
        linkedList = _calculate2_2.mainCalculate( tower)
        linkedListsByName[tower.name] = linkedList


    _output.mainOutput(linkedListsByName)

        

if __name__ == "__main__": main()