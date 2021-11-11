# Author Jacobus Crawford
# written 11/9/2021


def playPhaseTen():
    while(1):
        hand = getInput()
        if(len(hand) < 10): #should only happen with quit or test
            if(hand[0] == "quit"):
                return
            elif(hand[0] == "test"):
                runTestSuite() #run the test suite then go back to asking for input
                continue
        
        #print(hand)
        
        phasesMet = getPhases(hand)

        if(len(phasesMet) == 0):
            print("The hand",hand,"meets no phases. Try again.\n\n")
        else:
            print("The hand ",hand," meets phases ",phasesMet,". Well done!\n\n", sep = "")
        
        
    

def getInput():
    done = False
    while(not done):
        #get the user input
        hand = input("Please enter the ten cards of the hand with a space inbetween each (type quit as the first to exit)").split()

        #validate and cast the hand to integers
        newHand = validateHand(hand)
        
        if(len(newHand) == 0): #it "threw" an error
            continue
        else:
            return newHand

    #should never get here but doesn't hurt to be tidy
    return ["quit"]



#checks and returns the hand in numbers if valid, returns an empty hand if not valid
def validateHand(hand):
    if(len(hand) == 0):
        print("Hand has no cards. Please enter 10 cards.\n")
        return []
    
    if(hand[0].lower() == "quit" or hand[0].lower() == "q"):
        return ["quit"] #tells the program to quit as invalid numebr of items

    if(hand[0].lower() == "test" or hand[0].lower() == "t"):
        return ["test"] #tells the program to run the test suite
    
    #check if they gave us the right number of cards
    handLen = len(hand)
    if(handLen != 10):
        if(handLen < 10):
            print("Hand only has",handLen,"cards. Please enter 10 cards.\n")
            return []
        else:
            print("Hand has",handLen,"cards. Please enter only 10 cards.\n")
            return []

    #check validity of each card
    newHand = []
    for i in hand:
        #check that they entered numbers
        try:
            card = int(i)
        except ValueError:
            print(i,"is not a valid card. Please enter integers for card values.\n")
            break
        
        #check that they entered valid numbers
        if(card < 1 or card > 12):
            print(i,"is not a valid card. Please enter numbers from 1 to 12.\n")
            break

        #add it to the hand if valid
        newHand.append(card)
        
    else: #if we finish without errors return the hand
        #check that we aren't cheating (too many cards of the same number)
        for i in newHand:
            if(newHand.count(i) > 8):
                print("Hey now, no cheating. You have more ",i,"'s than is possible in the game.\n",sep="") 
                break
        else:    
            return newHand

    #default catch all for errors
    return []




def getPhases(hand):
    phasesMet = []

    #phase 1: 2 sets of 3
    if(meetsSetPhase(hand,3,3)):
        phasesMet.append(1)

    #phase 2: set of 3 and run of 4
    if(meetsRunPhase(hand,3,4)):
        phasesMet.append(2)

    #phase 3: set of 4 and run of 4
    if(meetsRunPhase(hand,4,4)):
        phasesMet.append(3)

    #phase 6: run of 9 (satisfies 4 and 5 as well)
    if(meetsRunPhase(hand,0,9)):
        phasesMet.extend([4,5,6])

        #phase 5: run of 8 (satisfies 4 as well)
    elif(meetsRunPhase(hand,0,8)):
        phasesMet.extend([4,5])

        #phase 4: run of 7
    elif(meetsRunPhase(hand,0,7)):
        phasesMet.append(4)

    #phase 7: 2 sets of 4
    if(meetsSetPhase(hand,4,4)):
        phasesMet.append(7)

    #phase 8 is not included

    #phase 9: set of 5 and set of 2
    if(meetsSetPhase(hand,5,2)):
        phasesMet.append(9)

    #phase 10: set of 5 and set of 3
    if(meetsSetPhase(hand,5,3)):
        phasesMet.append(10)

    return phasesMet

    


#determins if it meets the phase with two sets of firstNum and secondNum
def meetsSetPhase(hand,firstNum,secondNum):

    #always make sure the first one to run is bigger (or equal)
    if(secondNum > firstNum):
        temp = firstNum
        firstNum = secondNum
        secondNum = temp
    
    firstSet = hasValidSet(hand,firstNum)
    
    if(len(firstSet) == 0):
        return False #there is not a satisfactory set for the first

    #remove the first set from what to consider for the second set
    setHand = hand.copy()
    for i in firstSet:
        setHand.remove(i)

    secondSet = hasValidSet(setHand, secondNum)
    if(len(secondSet) == secondNum):
        return True #we've found something that meets both sets

    return False


#determins if it meets the phase with a run of runnum and a set of setnum
# a value of 0 means there is no requirement for that value in this phase
def meetsRunPhase(hand,setNum,runNum):
    
    if(runNum > 0): #if we're delaing with something with a run in it
        curHand = hand.copy()
        done = False
        
        while(not done):
            outRun = hasValidRun(curHand,runNum)
            
            if(len(outRun) == 0):
                return False #there is not a satisfactory run
            
            
            #remove the run from what to consider for the set
            setHand = hand.copy()
            for i in outRun:
                setHand.remove(i)

            outSet = hasValidSet(setHand, setNum)
            if(len(outSet) == setNum):
                return True #we've found something that meets the set and run

            #make the new "hand" to consider for the next run, will always be
            #smaller than the previous hand, therfore guaranteeing exit condition
            curHand = []
            leastRun = outRun[0]
            for i in hand:
                if(i > leastRun):
                    curHand.append(i)

            if(len(curHand) > runNum + setNum):
                return False #impossible to meet both conditions
            
    else: # just dealing with a set
        outSet = hasValidSet(hand, setNum)
        if(len(outSet) == setNum):
            return True #we found the set

    #catch all
    return False
            



#determins if there is a valid run of runnum cards in the hand
# hand is the cards (sorted), runnum is the number of cards needed in the run
# returns the first run that is valid if any, otherwise returns an empty list
def hasValidRun(hand,runNum):
    if(len(hand) < runNum or runNum < 1):
        return [] #sanity check

    #get rid of duplicates and sort
    newHand = list(set(hand))
    
    i = 0
    while i < len(newHand):
        if(i + runNum > len(newHand)):
            return [] #impossible to get a valid run from this point
        
        runStart = newHand[i]
        run = range(runStart, runStart + runNum)
        
        j = 0
        found = True
        while j < runNum:
            #check if the hand matches the run
            
            if(newHand[i + j] != run[j]):
                found = False
                break
            j += 1
            
        if(found): #found a valid run
            return run
        
        #if broken returns to top and tries again
        i += 1

    #didn't find a valid run
    return []



#determins if there is a valid set of setnum cards in the hand
#hand is the cards (sorted), setnum is the number of cards needed in the set
#returns the first valid set if any, otherwise an empty list
def hasValidSet(hand,setNum):
    if(len(hand) < setNum or setNum < 1):
        return [] #sanity check
    
    for i in hand:
        #check if the current value has enough to be the set
        if(hand.count(i) >= setNum):
            #found the set, create it and return it
            outSet = []
            for j in range(setNum):
                outSet.append(i)
            return outSet

    #didn't find a set
    return []



def runTestSuite():
    print("\nRunning input tests -------------------------------------------\n")
    runInputTests()
    print("Finished input tests ------------------------------------------\n\n")

    print("\nRunning set tests ---------------------------------------------\n")
    runSetTests()
    print("Finished set tests --------------------------------------------\n\n")

    print("\nRunning run tests ---------------------------------------------\n")
    runRunTests()
    print("Finished run tests --------------------------------------------\n\n")

    print("\nRunning set phase tests ---------------------------------------\n")
    runSetPhaseTests()
    print("Finished set phase tests --------------------------------------\n\n")

    print("\nRunning run phase tests ---------------------------------------\n")
    runRunPhaseTests()
    print("Finished run phase tests --------------------------------------\n\n")
    
    print("\nRunning play tests --------------------------------------------\n")
    runPlayTests()
    print("Finished play tests -------------------------------------------\n\n")



def runInputTests():
    hands = []
    expectedResults = []

    #start hand/expected pairs ---------------------------------------------

    #1 test exit condition
    hands.append(["quit"])
    expectedResults.append(["quit"])

    #2 test exit condition
    hands.append(["Quit"])
    expectedResults.append(["quit"])

    #3 test exit condition
    hands.append(["q"])
    expectedResults.append(["quit"])

    #4 test exit condition
    hands.append(["Q"])
    expectedResults.append(["quit"])

    #5 test test condition
    hands.append(["test"])
    expectedResults.append(["test"])

    #6 test test condition
    hands.append(["Test"])
    expectedResults.append(["test"])

    #7 test test condition
    hands.append(["t"])
    expectedResults.append(["test"])

    #8 test test condition
    hands.append(["T"])
    expectedResults.append(["test"])

    #9 test too few cards
    hands.append(["1"])
    expectedResults.append([])

    #10 test too many cards
    hands.append(["1","1","1","1","1","1","1","1","1","1","1","1"])
    expectedResults.append([])

    #11 test text in input
    hands.append(["1","a","2","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #12 test quit in input
    hands.append(["q","1","2","1","2","1","2","1","2","1"])
    expectedResults.append(["quit"])

    #13 test quit in invalid slot
    hands.append(["1","q","2","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #14 test test in input
    hands.append(["t","1","2","1","2","1","2","1","2","1"])
    expectedResults.append(["test"])

    #15 test test in invalid slot
    hands.append(["1","t","2","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #16 test float in input
    hands.append(["11.3","1","2","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #17 test invalid number
    hands.append(["1","13","2","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #18 test invalid number
    hands.append(["1","2","0","1","2","1","2","1","2","1"])
    expectedResults.append([])

    #19 test cheating
    hands.append(["1","1","1","1","1","1","1","1","1","1"])
    expectedResults.append([])

    #20 test no hand
    hands.append([])
    expectedResults.append([])

    #21 test valid
    hands.append(["1","2","3","4","5","6","7","8","9","1"])
    expectedResults.append([1,2,3,4,5,6,7,8,9,1])

    
    ## test
    #hands.append([])
    #expectedResults.append([])

    #end hand/expected pairs ------------------------------------------------

    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        expectedResult = expectedResults[i]

        print("testing hand",i+1)

        testResult = validateHand(hand)

        if(testResult == expectedResult):
            print(hand,"PASSED test. Result",testResult,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Result",testResult,"did not match expected",expectedResult,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")



def runSetTests():
    hands = []
    setNums = []
    expectedResults = []

    #start hand/expected pairs ---------------------------------------------

    #1 test no set
    hands.append([1,2,3,4,5,6,7,8,9,10])
    setNums.append(3)
    expectedResults.append([])

    #2 test set not long enough
    hands.append([1,1,1,2,3,4,5,6,7,8])
    setNums.append(5)
    expectedResults.append([])

    #3 test valid set
    hands.append([1,1,1,2,3,4,5,6,7,8])
    setNums.append(3)
    expectedResults.append([1,1,1])

    #4 test mixed up set
    hands.append([2,1,3,1,4,5,6,7,8,1])
    setNums.append(3)
    expectedResults.append([1,1,1])


    ## test
    #hands.append([])
    #setNums.append()
    #expectedResults.append([])

    #end hand/expected pairs ------------------------------------------------

    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        setNum = setNums[i]
        expectedResult = expectedResults[i]

        print("testing hand",i+1)

        testResult = hasValidSet(hand,setNum)

        if(testResult == expectedResult):
            print(hand,"PASSED test. Result for set of",setNum,",",testResult,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Result",testResult,"did not match expected for set of",setNum,",",expectedResult,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")


def runRunTests():
    hands = []
    runNums = []
    expectedResults = []

    #start hand/expected pairs ---------------------------------------------

    #1 test no run
    hands.append([1,1,3,3,5,5,7,7,9,9])
    runNums.append(3)
    expectedResults.append([])

    #2 test run not long enough
    hands.append([1,1,1,1,2,3,4,6,7,8])
    runNums.append(5)
    expectedResults.append([])

    #3 test valid run
    hands.append([1,1,1,2,3,4,5,6,7,8])
    runNums.append(4)
    expectedResults.append(range(1,5))

    #4 test mixed up run
    hands.append([2,1,3,1,4,5,6,7,8,1])
    runNums.append(4)
    expectedResults.append(range(1,5))


    ## test
    #hands.append([])
    #runNums.append()
    #expectedResults.append([])

    #end hand/expected pairs ------------------------------------------------

    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        runNum = runNums[i]
        expectedResult = expectedResults[i]

        print("testing hand",i+1)

        testResult = hasValidRun(hand,runNum)

        if(testResult == expectedResult):
            print(hand,"PASSED test. Result for run of",runNum,",",testResult,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Result",testResult,"did not match expected for run of",runNum,",",expectedResult,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")



def runSetPhaseTests():
    hands = []
    setNums = []
    expectedResults = []

    #start hand/expected pairs ---------------------------------------------

    #1 test no sets
    hands.append([1,2,3,4,5,6,7,8,9,1])
    setNums.append([3,3])
    expectedResults.append(False)

    #2 test one set
    hands.append([1,1,1,2,3,4,5,6,7,8])
    setNums.append([3,3])
    expectedResults.append(False)

    #3 test one set within the second
    hands.append([1,1,1,1,1,2,3,4,5,6])
    setNums.append([5,3])
    expectedResults.append(False)

    #4 test valid
    hands.append([1,1,1,1,1,1,1,1,2,2])
    setNums.append([5,3])
    expectedResults.append(True)

    #5 test valid with numbers backwards
    hands.append([1,1,1,1,1,1,1,1,2,2])
    setNums.append([3,5])
    expectedResults.append(True)

    #6 test mixed up valid
    hands.append([1,2,1,3,2,4,5,2,6,1])
    setNums.append([3,3])
    expectedResults.append(True)


    ## test
    #hands.append([])
    #setNums.append([])
    #expectedResults.append()

    #end hand/expected pairs ------------------------------------------------

    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        setNum = setNums[i]
        expectedResult = expectedResults[i]

        print("testing hand",i+1)

        testResult = meetsSetPhase(hand,setNum[0],setNum[1])

        if(testResult == expectedResult):
            print(hand,"PASSED test. Result for sets of",setNum,",",testResult,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Result",testResult,"did not match expected for sets of",setNum,",",expectedResult,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")




def runRunPhaseTests():
    hands = []
    runNums = []
    expectedResults = []

    #start hand/expected pairs ---------------------------------------------

    #1 test no valid run
    hands.append([1,1,1,1,2,2,2,2,4,4])
    runNums.append([0,4])
    expectedResults.append(False)

    #2 test set without run
    hands.append([1,1,1,1,2,2,2,2,4,4])
    runNums.append([4,4])
    expectedResults.append(False)

    #3 test run without set
    hands.append([1,2,3,4,5,6,7,8,9,1])
    runNums.append([4,4])
    expectedResults.append(False)

    #4 test not long enough run
    hands.append([1,2,3,4,1,1,1,2,2,2])
    runNums.append([0,7])
    expectedResults.append(False)

    #5 test set and run dependent on same number
    hands.append([1,1,1,1,2,3,4,6,7,8])
    runNums.append([4,4])
    expectedResults.append(False)

    #6 test valid
    hands.append([1,1,1,1,2,3,4,5,7,7])
    runNums.append([4,4])
    expectedResults.append(True)

    #7 test valid mixed up
    hands.append([7,1,5,2,1,3,4,1,7,1])
    runNums.append([4,4])
    expectedResults.append(True)
    

    ## test
    #hands.append([])
    #runNums.append([])
    #expectedResults.append()

    #end hand/expected pairs ------------------------------------------------

    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        runNum = runNums[i]
        expectedResult = expectedResults[i]

        print("testing hand",i+1)

        testResult = meetsRunPhase(hand,runNum[0],runNum[1])

        if(testResult == expectedResult):
            print(hand,"PASSED test. Result for [set,run] of",runNum,",",testResult,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Result",testResult,"did not match expected for [set,run] of",runNum,",",expectedResult,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")



def runPlayTests():
    hands = []
    solutions = []

    #start hand/solution pairs ---------------------------------------------

    #1 test nothing
    hands.append([1,3,4,6,7,9,10,1,12,3])
    solutions.append([])

    #2 test that the 1 cannot be used in both the set and run
    hands.append([1,1,1,2,3,4,6,8,10,12])
    solutions.append([])

    #3 test phase 1
    hands.append([1,1,1,2,2,2,3,3,4,4])
    solutions.append([1])

    #4 test phase 2
    hands.append([1,1,1,3,4,5,6,8,9,9])
    solutions.append([2])

    #5 test phase 2 randominzed hand
    hands.append([6,1,4,1,5,3,8,9,1,9])
    solutions.append([2])

    #6 test phase 2 and 3 (can't exclusively test 3)
    hands.append([1,1,1,1,2,3,4,5,7,8])
    solutions.append([2,3])

    #7 test phase 4
    hands.append([1,2,3,4,5,6,7,9,9,10])
    solutions.append([4])

    #8 test phase 4 and 5 (can't exclusively test 5)
    hands.append([1,2,3,4,5,6,7,8,10,10])
    solutions.append([4,5])

    #9 test phase 4, 5, and 6 (can't exclusively test 6)
    hands.append([1,2,3,4,5,6,7,8,9,11])
    solutions.append([4,5,6])

    #10 test phase 1 and 7 (can't exclusively test 7)
    hands.append([1,1,1,1,2,2,2,2,4,4])
    solutions.append([1,7])

    #11 test phase 9
    hands.append([1,1,1,1,1,2,2,4,6,8])
    solutions.append([9])

    #12 test phase 1, 9, and 10 (can't exclusively test 10)
    hands.append([1,1,1,1,1,2,2,2,4,6])
    solutions.append([1,9,10])

    #13 test given test case
    hands.append([1,2,3,4,5,6,7,8,8,8])
    solutions.append([2,4,5])

    ## test
    #hands.append([])
    #solutions.append([])

    #end hand/solution pairs ------------------------------------------------
    
    i = 0
    passed = 0
    failed = 0
    while i < len(hands):
        hand = hands[i]
        solution = solutions[i]

        print("testing hand",i+1)

        testSolution = getPhases(hand)

        if(testSolution == solution):
            print(hand,"PASSED test. Solution",testSolution,"matched\n")
            passed += 1
        else:
            print(hand,"FAILED test.")
            print("Solution",testSolution,"did not match expected",solution,"\n")
            failed += 1
            
        i += 1

    print(i,"tests run")
    print("PASSED ",passed," / ",i,sep="")
    print("FAILED ",failed," / ",i,sep="")
    print("")

    

playPhaseTen()
