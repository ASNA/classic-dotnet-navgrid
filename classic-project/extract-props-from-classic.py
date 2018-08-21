
import sys
import re
from enum import Enum

class State(Enum):
    limbo = 0
    inControl = 1
    inForm = 2
    inOwnerProperty = 3


def getFileLines(fileName):
    codeLines = []
    with open(fileName) as f:
        lines = f.readlines()    
        
    for line in lines:     
        codeLines.append(line.replace("\t", "    "))
        
    return codeLines                  
    
def processLines(lines):
    state = State.limbo 
    reservedPropertyNames = ['Version', 'LicKey', 'ServerName', 'AllowClearReset', 'DftPropType', 'Charset']
    controlName = ''
    for line in lines:
        # matchObj = re.match(r'^DCL', line)
        startsWithDCLCTL = re.match(r'^DCL.*\/\/\s*(.*)?$', line)        
        if startsWithDCLCTL:
            state = State.inControl
            controlName = startsWithDCLCTL.group(1) 
            print('---------------------------')
            print(controlName)
            continue

        if state == State.inControl:             
            startsWithINITPROP = re.match(r'^INITPROP.*NAME\((.*?)[)].*TYPE\((.*?)[)].*VALUE\((.*?)[)]', line)
            if startsWithINITPROP:
                propName = startsWithINITPROP.group(1)                
                if not propName.startswith('_') and not propName in reservedPropertyNames:
                    propType = startsWithINITPROP.group(2)                
                    propValue = startsWithINITPROP.group(3)                
                    print(propName + ' = '+ propValue)

        startsWithENDPROP = re.match(r'^ENDPROP', line)
        if startsWithDCLCTL:
            state = State.limbo

if len(sys.argv) == 1:
    print("Useage:")
    print("    replace-chars.py {filename}")
    exit()

fileName = sys.argv[1]    
# fileName = 'formMain.vrf'

lines = getFileLines(fileName)
processLines(lines)



#outfile = open(fileName + ".annotated", 'w')
#for line in lines:
#    outfile.write(line)            

