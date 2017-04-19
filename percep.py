import fileinput
import copy

#Global variable that stores the dataset in a list of lists
trainingSet = []
testingSet = []
#wSet = [-0.00999999999999999, 0.1, 0.1]
wSet = [0.1, 0.1, 0.1]
#wSet = [-0.5, 1, 1]
nValue = 0.01
inputs = 0
trainingRows = 0
testRows = 0
threshold = 0
maxIterations = 1000
#Dataset parsing as training set
def readData():
    global inputs, trainingRows, testRows;
    input =  fileinput.input();
    state = 0
    countRows = 0;
    for line in input:
        if state == 0:
            inputs = int(line.strip("\n").strip("\r"))
            state += 1
            continue
        if state == 1:
            trainingRows = int(line.strip("\n").strip("\r"))
            state += 1
            continue
        if state == 2:
            testRows = int(line.strip("\n").strip("\r"))
            state += 1
            continue
        if state == 3 and countRows < trainingRows:
            trainingSet.append(line.replace(" ","").strip("\n").strip("\r").split(","))
            trainingSet[countRows].insert(0,'1')
            countRows += 1
            if countRows >= trainingRows:
                countRows = 0
                state += 1
                continue
        if state == 4:
            testingSet.append(line.replace(" ","").strip("\n").strip("\r").split(","))
            testingSet[countRows].insert(0,'1')
            countRows += 1


def calculateOuput(xRow):
    result = float(0)
    global threshold

    i = 0
    for w in wSet:
        result += w * float(xRow[i])
        i += 1

    if result > threshold:
        return 1
    else:
        return 0


def updateW(xRow, d, y):
    global nValue
    for i in range(0, 3):
        wSet[i] = wSet[i] + nValue * (d - y) * float(xRow[i])
        i += 1


def rule():
    errors = 0
    currentIterations = 0
    global maxIterations
    for i in range(0, maxIterations):
        for row in trainingSet:
            xVector = copy.copy(row)
            xVector.pop
            d = float(xVector[3])
            res = calculateOuput(xVector)
            if res != d:
                errors += 1
                updateW(xVector, d, res)
                break
    #print "errors: ", errors
    if errors >= maxIterations:
        print "no solution found"

def testing():
    for row in testingSet:
        print calculateOuput(row)


readData()
#print inputs, trainingRows, testRows
#print trainingSet
#print testingSet
rule()
#print wSet
testing()
