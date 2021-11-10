
def playPhaseTen():
    while(1):
        hand = getInput()
        if(len(hand) < 10): #should only happen with quit
            return
        
        #print(hand)
        
        getPhases(hand)
        
        
    

def getInput():
    done = False
    while(not done):
        #get the user input
        hand = input("Please enter the ten cards of the hand with a space inbetween each (put quit as the first to exit)").split()

        if(len(hand) == 0):
            print("Hand only has no cards. Please enter 10 cards.\n")
            continue
        
        if(hand[0].lower() == "quit" or hand[0].lower() == "q"):
            return ["quit"] #tells the program to quit as invalid numebr of items

        #check if they gave us the right number of cards
        handLen = len(hand)
        if(handLen != 10):
            if(handLen < 10):
                print("Hand only has",handLen,"cards. Please enter 10 cards.\n")
                continue
            else:
                print("Hand has",handLen,"cards. Please enter only 10 cards.\n")
                continue

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

    #should never get here but doesn't hurt to be tidy
    return ["quit"]




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

    if(len(phasesMet) == 0):
        print("The hand",hand,"meets no phases. Try again.\n\n")
    else:
        print("The hand ",hand," meets phases ",phasesMet,". Well done!\n\n", sep = "")

    


#determins if it meets the phase with two sets of firstNum and secondNum
def meetsSetPhase(hand,firstNum,secondNum):

    #print(hand)

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

    #print(hand)
    
    if(runNum > 0): #if we're delaing with something with a run in it
        curHand = hand.copy()
        done = False
        
        while(not done):
            outRun = hasValidRun(curHand,runNum)
            
            if(len(outRun) == 0):
                return False #there is not a satisfactory run
            #print(outRun,len(outRun),runNum)
            
            #remove the run from what to consider for the set
            setHand = hand.copy()
            for i in outRun:
                setHand.remove(i)

            #print(setHand)

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
        #print("run",run)
        #print(runNum)
        j = 0
        found = True
        while j < runNum:
            #check if the hand matches the run
            #print(newHand[i+j],run[j])
            if(newHand[i + j] != run[j]):
                found = False
                break
            j += 1
            
        if(found): #found a valid run
            #print("retunring")
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


playPhaseTen()
