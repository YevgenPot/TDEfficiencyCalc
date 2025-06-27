import _inputModule
import _processing
import _calculate2

def main():
    towers_data = _inputModule.mainInput()
    towers_list = _processing.mainProcess(towers_data)

    for i in range(len(towers_list)):
        _calculate2.mainCalculate( towers_list[i] )
        

if __name__ == "__main__": main()