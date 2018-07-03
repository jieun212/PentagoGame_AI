'''
TCSS 435 - PA 2. Pentago
Implement Minmax & Alpha-Beta pruning

@author: Jieun Lee (jieun212@uw.edu)
@version: May 07, 2017
'''


from sys import maxint 
import random
import time
from copy import deepcopy
from collections import deque


MIN_INT = (-1 * maxint) - 1
MAX_INT = maxint

# algorithm = "Minmax"      # <----- Choose the algorithm this
algorithm = "AlphaBeta"     # <----- or this

maxDepth = 2    # <----- Change the value for maximum depth level


def main():
    
    global player1
    global player2
    global outputFile
    
    # Open Output.txt file to write the game information
    outputFile = open("Output.txt", 'w')
    
    # Set players with name and token color
    pentagoBot = Player()
    human = Player()
    
    # Computer player
    pentagoBot.name = "PentagoBot"
    pentagoBot.token = 'w'
    pentagoBot.isBot = True
    
    # Human player
    human.isBot = False
    while True:
        human.name = raw_input("Enter your name: ")
        if (human.name != None and len(human.name) > 0):
            break
    while True:
        human.token = raw_input("Enter token color, w or b: ").lower()
        if(human.token.lower() != 'w' and human.token.lower() != 'b'):
            print ("Wrong input. Enter w or b without quotation marks")
        else:
            break
    if (human.token  == 'w'):
        pentagoBot.token = 'b'
     
     
    # Choose the first player randomly
    random.seed()
    randomValue = random.randint(1, 2)
         
    if (randomValue == 1):
        player1 = human
        player2 = pentagoBot
    else:
        player1 = pentagoBot
        player2 = human
        
         
    player1.isFirst = True
     
    # Display players information
    print ('\n' + human.name)
    print (pentagoBot.name)
    print (human.token)
    print (pentagoBot.token)
    print ("You (Human) are player " + str(randomValue) + '\n')
    
    # write players information to the text file
    outputFile.write(human.name + '\n')
    outputFile.write(pentagoBot.name + '\n')
    outputFile.write(human.token + '\n')
    outputFile.write(pentagoBot.token + '\n')
    outputFile.write("You (Human) are player " + str(randomValue) + '\n')
    
    # Display numbered board
#     displayNumberedBoard()
    
    # Initialize and display game board
    gameBoard = [[0 for i in range(6)] for j in range(6)]
    for r in range (0, 6):
        for c in range (0, 6):
            gameBoard[r][c] = '.'
    

    board_str = displayBoard(gameBoard)
    print (board_str)
    
    
    # Play the game
    play(gameBoard)
    
    # Close the output file
    outputFile.close()
    
    
# Play the game and write the game on the given file
def play(gameBoard):
    
    global player1
    global player2
    global outputFile
    
    # List of moves made, in order from 1st to last, alternating players
    moveList = list()
    
    # The total number of positions that players can put their tokens
    availablePosition = 36;
    currentPlayer = player1
    
    countWinner = [2]
    
    while True:
        
        # If current player is AI, get a token place using minmax or a-b pruning algorithm
        if (currentPlayer.isBot):
            if (algorithm == "Minmax"):
                place = minmax_decision(gameBoard, currentPlayer)
            elif (algorithm == "AlphaBeta"):
                place = alpha_beta_decision(gameBoard, currentPlayer)
            
            # Display the token place & write the place 
            place_str = currentPlayer.name + ": " + place
            print (place_str)
            outputFile.write('\n\n' + place_str + '\n')
            
        else:
            # If the player is human, ask the token position
            place = raw_input(currentPlayer.name + ": ")
            while (not isValidPlace(place)):
                place = raw_input(currentPlayer.name + ": ")
                
            outputFile.write('\n\n' + currentPlayer.name + ": " + place + '\n')   
        
        
        block = int(place[0]) - 1
        position = int(place[2]) - 1
        
        # if current player is human, check the input place
        if (currentPlayer.isBot):
            checkAvailable = True
        else:
            checkAvailable = isPositionAvailable(gameBoard, block, position)
             
         
        # If the input place is valid, place and rotate
        if (availablePosition > 0 and checkAvailable):
            
            moveList.append(place)
            
            # place the current player's token on the game board
            row = (block / 2 * 3)  + position / 3
            col = (block % 2 * 3) + position % 3
            
            gameBoard[row][col] = currentPlayer.token
            
            # Decrease the available positions to place token
            availablePosition = availablePosition - 1
                
            countWinner = checkWinner(gameBoard)
            w_count = countWinner[0]
            b_count = countWinner[1]
            hasWinner = False
            if (w_count > 0 or b_count > 0):
                hasWinner = True
                
            # rotate the game board
            rotateBlock = int(place[4])
            rotateDirection = place[5]
            gameBoard = deepcopy(rotateBoard(gameBoard, rotateBlock, rotateDirection))
            
            # After rotated the board, check if there is winner(s)
            countWinner = checkWinner(gameBoard)
            w_count += countWinner[0]
            b_count += countWinner[1]
            if (hasWinner or (w_count > 0 or b_count > 0)):
                break
            
            # Display and write board configuration and expanded states list
            board_str = displayBoard(gameBoard)
            print (board_str)
            print (moveList)
            print ('\n')
            
            outputFile.write(str(board_str) + '\n')
            outputFile.write('\n' + str(moveList))
            
            # Switch current player
            if (currentPlayer.token == player1.token):
                currentPlayer = player2
            else:
                currentPlayer = player1
        
        elif (not checkAvailable):
            print("Cannot place your token! Try again.")
        
        elif (availablePosition <= 0):
            # if there in no more position to place a token, then stop the game
            break


    # Get who is the winner
    if (w_count == 0 and b_count > 0):
        winner = 'b'
    elif (w_count > 0 and b_count == 0):
        winner = 'w'
    else:
        winner = 't'
        
    # Display game result
    board_str = displayBoard(gameBoard)
    print (board_str)
    print (moveList)
    outputFile.write(str(board_str) + '\n')
    outputFile.write('\n' + str(moveList))
    
    print ('\n\n-- GAME OVER --')
    winner_str = ""
    if (player1.token.lower() == winner.lower()):
        winner_str = 'Winner: ' + player1.name
    elif (player2.token.lower() == winner.lower()):
        winner_str = 'Winner: ' + player2.name
    else:
        winner_str = 'Tied!'
    print (winner_str)
    
    outputFile.write('\n\n' + winner_str + '\n')







# Decide which value is the best value for the pentagoBot
# It returns operator that corresponding to the best possible place(move)
def minmax_decision(state, pentagoBot):

    # Create child nodes (operators) of root
    currentNode = createMinmaxGameTree(state, pentagoBot.token)
    
    startTime = time.clock()

    indexOfMinmaxValue = 0
    if (pentagoBot.isFirst):  # if the bot is the 1st player, get MAX value for next place of AI      
        minmaxValue = MIN_INT
        for op in range(len(currentNode.children)):
            value = minmax_value(pentagoBot, pentagoBot.isFirst, currentNode.children[op])
            if (value > minmaxValue):
                minmaxValue = value
            indexOfMinmaxValue = op
    else: # if the bot is the 2nd player, get MIN value for next place of AI
        minmaxValue = MAX_INT
        for op in range(len(currentNode.children)):
            value = minmax_value(pentagoBot, pentagoBot.isFirst, currentNode.children[op])
            if (value < minmaxValue):  
                minmaxValue = value
                indexOfMinmaxValue = op
        
    # record elapsed time
    totalTime = time.clock() - startTime
    
    print ("[Minmax] Elapsed time: {0} s".format(totalTime))
        
    return currentNode.children[indexOfMinmaxValue].place

# Return value of the state. It goes through the whole game
def minmax_value(pentagoBot, isMaxPlayer, node):

    # Terminal state
    if (node.depth == maxDepth):
        return utility(pentagoBot, node.data)

    # If pentagoBot is the 1st player, get max value
    if (isMaxPlayer):
        # get the highest value of successors(children)
        value = MIN_INT
        for child in node.children:
            value = max(value, minmax_value(pentagoBot, False, child))
        return value
    
    else: # If pentagoBot is the 2nd player, get min value
        # get the lowest value of successors(children)
        value = MAX_INT
        for child in node.children:
            value = min(value, minmax_value(pentagoBot, True, child))
        return value

# Create a game tree with given state
def createMinmaxGameTree(state, pentagoBotToken):
    
    # create root node with initial state
    root = Node()
    root.data = state
    root.depth = 0
    
    parentNode = root
    
    # fringe = Queue (expand node from left to right)
    queue = deque()
    
    # Get the token of PentagoBot
    if (pentagoBotToken == 'b'):
        pentago = 'b'
        human = 'w'
    else:
        pentago = 'w'
        human = 'b'
    
    # Count how many nodes are expanded
    count_expanded = 0;
    
    while True:
        
        # create children nodes up to the maximum depth level
        if (parentNode.depth == maxDepth):
            break

        # Assign token color depends on the depth of the node
        # if depth is 0, 2, 4, 8,..., it's PentagoBot's turn
        # else it's human's turn
        if (parentNode.depth % 2 == 0):
            currentToken = pentago
        else: 
            currentToken = human

        # create children node (all possible actions)
        for block in range (0, 4):
            for position in range (0, 9):
                
                # if the position is available, then create child node
                if (isPositionAvailable(parentNode.data, block, position)):
                    
                    # Deep copy the parent state before creating children
                    copyParentBoard = deepcopy(parentNode.data)
                    
                    row = (block / 2 * 3) + position / 3
                    col = (block % 2 * 3) + position % 3
                
                    # place the current token on the game board
                    copyParentBoard[row][col] = currentToken
                    
                    for rotateBlock in range (1, 5):
                        for rotateDir in "lr":
                            
                            # rotate the game board
                            childBoard = deepcopy(copyParentBoard)
                            childBoard = deepcopy(rotateBoard(childBoard, rotateBlock, rotateDir))
                            
                            # create child node
                            childNode = Node()
                            childNode.data = childBoard
                            childNode.depth = parentNode.depth + 1
                            childNode.place = "{0}/{1} {2}{3}".format(block + 1, position + 1 , rotateBlock, rotateDir)
                            
                            count_expanded += 1
                            
                            # add the created childNode to the parentNode
                            parentNode.children.append(childNode)
                            
                            # add the created childeNode to the queue
                            queue.append(childNode)
                     
        # next parent node = dequeued element of the queue       
        parentNode = queue.popleft()

#     print ("count_expanded", count_expanded)
    return root





# Decide which value is the best value for the pentagoBot
# It returns operator that corresponding to the best possible place(move)
def alpha_beta_decision(state, pentagoBot):
    
    global count_expanded 
    count_expanded = 0
    
    # Create child nodes (operators) of root
    rootNode = Node()
    rootNode.data = state
    rootNode.depth = 0

    startTime = time.clock()
     
    indexOfMinmaxValue = 0
    
    rootNode.value = alpha_beta_valule(rootNode, pentagoBot, pentagoBot.isFirst, MIN_INT, MAX_INT)
    for op in range(len(rootNode.children)):
        if (rootNode.children[op].value == rootNode.value):
            indexOfMinmaxValue = op
            break

    # record elapsed time
    totalTime = time.clock() - startTime            
    
#     print ("[a-b Pruning] Elapsed time: {0} ms".format(totalTime))
#     print ("count_expanded", count_expanded)

    return rootNode.children[indexOfMinmaxValue].place


# Create a game tree with given state and returns the minmax value for alpha-beta pruning
def alpha_beta_valule(parentNode, pentagoBot, isMaxPlayer, alpha, beta):

    global count_expanded
    
    # Get the token of PentagoBot
    if (pentagoBot.token == 'b'):
        humanToken = 'w'
    else:
        humanToken = 'b'
        
    if (parentNode.depth % 2 == 0):
        childToken = humanToken
    else: 
        childToken = pentagoBot.token

    # create children node (all possible actions)
    for block in range (0, 4):
        
        for position in range (0, 9):
            
            # if the position is available, then create child node
            if (isPositionAvailable(parentNode.data, block, position)):
                
                # Deep copy the parent state before creating children
                copyParentBoard = deepcopy(parentNode.data)
                
                row = (block / 2 * 3) + position / 3
                col = (block % 2 * 3) + position % 3
            
                # place the current token on the game board
                copyParentBoard[row][col] = childToken
                
                for rotateBlock in range (1, 5):
                    
                    for rotateDir in "lr":
                        
                        # rotate the game board
                        childBoard = deepcopy(copyParentBoard)
                        childBoard = deepcopy(rotateBoard(childBoard, rotateBlock, rotateDir))
                        
                        # create child node
                        childNode = Node()
                        childNode.data = childBoard
                        childNode.depth = parentNode.depth + 1
                        childNode.place = "{0}/{1} {2}{3}".format(block + 1, position + 1 , rotateBlock, rotateDir)
                        
                        # Counts expanded node
                        count_expanded += 1
                        
                        # add the created childNode to the parentNode
                        parentNode.children.append(childNode)
                        
                        # Terminal state
                        if (childNode.depth == maxDepth):
                            return utility(pentagoBot, childNode.data)

                        # Get and set the value of the child node
                        childNode.value = alpha_beta_valule(childNode, pentagoBot, not isMaxPlayer, alpha, beta)
                        


                        value = childNode.value

                        if (isMaxPlayer): # if parent node == max node
                            if (value >= beta):
                                return value
                            else:
                                alpha = max (value, alpha)
                        else: # if parent node == min node
                            if (value <= alpha):
                                return value
                            else:
                                beta = min (value, beta)

    return value





# Count how many tokens in row and assign a reasonable utility value
# (This utility value is NOT pretty good.)
def utility(pentagoBot, state):

    w_value = 0
    b_value = 0

    checkList = [5]
    
    # check horizontally
    for r in range (0, 5):
        for c in range (0, 2):
            checkList = state[r][c : c + 5]
            w_count = 0
            b_count = 0
            for i in range (0, len(checkList)):
                if (checkList[i] == 'w'):
                    w_count += 1
                elif (checkList[i] == 'b'):
                    b_count += 1

            # if there are 5 'w's in row
            if (w_count == 5):
                w_value += 100
            else:
                w_value += pow(w_count, 2)
            
            # if there are 5 'b's in row
            if (b_count == 5):
                b_value += 100
            else:
                b_value += pow(b_count, 2)
                
            checkList = []
    

    # check vertically
    checkList = []
    for c in range (0, 6):
        for r in range (0, 2):
            checkList.append(state[r][c])
            checkList.append(state[r + 1][c])
            checkList.append(state[r + 2][c])
            checkList.append(state[r + 3][c])
            checkList.append(state[r + 4][c])
            w_count = 0
            b_count = 0
            for i in range (0, len(checkList)):
                if (checkList[i] == 'w'):
                    w_count += 1
                elif (checkList[i] == 'b'):
                    b_count += 1
                
            # if there are 5 'w's in row
            if (w_count == 5):
                w_value += 100
            else:
                w_value += pow(w_count, 2)
            
            # if there are 5 'b's in row
            if (b_count == 5):
                b_value += 100
            else:
                b_value += pow(b_count, 2)
                    
            checkList = []  

    # check diagonally 
    for r in range (0, 2):
        for c in range (0, 2): 
            checkList.append(state[r][c])
            checkList.append(state[r + 1][c + 1])
            checkList.append(state[r + 2][c + 2])
            checkList.append(state[r + 3][c + 3])
            checkList.append(state[r + 4][c + 4])
            w_count = 0
            b_count = 0
            for i in range (0, len(checkList)):
                if (checkList[i] == 'w'):
                    w_count += 1
                elif (checkList[i] == 'b'):
                    b_count += 1
                
            # if there are 5 'w's in row
            if (w_count == 5):
                w_value += 100
            else:
                w_value += pow(w_count, 2)
            
            # if there are 5 'b's in row
            if (b_count == 5):
                b_value += 100
            else:
                b_value += pow(b_count, 2)
                    
            checkList = []

    checkList = []
    for r in range (4, 6):
        for c in range (0, 2): 
            checkList.append(state[r][c])
            checkList.append(state[r - 1][c + 1])
            checkList.append(state[r - 2][c + 2])
            checkList.append(state[r - 3][c + 3])
            checkList.append(state[r - 4][c + 4])
            w_count = 0
            b_count = 0
            for i in range (len(checkList)):
                if (checkList[i] == 'w'):
                    w_count += 1
                elif (checkList[i] == 'b'):
                    b_count += 1
                
            # if there are 5 'w's in row
            if (w_count == 5):
                w_value += 100
            else:
                w_value += pow(w_count, 2)
            
            # if there are 5 'b's in row
            if (b_count == 5):
                b_value += 100
            else:
                b_value += pow(b_count, 2)
                    
            checkList = []


    # if the pentagoBot's token is the first player
    if (pentagoBot.isFirst):
        if (pentagoBot.token == 'b'):
            return b_value - w_value
        else:
            return w_value - b_value 
    else:
        if (pentagoBot.token == 'b'):
            return w_value - b_value
        else:
            return b_value - w_value





# Check if there is a winner or winners
def checkWinner(state):
    
    w_count = 0
    b_count = 0
    checkList = [5]
    
    # check horizontally
    for r in range (0, 6):
        for c in range (0, 2):
            checkList = state[r][c : c + 5]
            if (all(x == 'w' for x in checkList)):
                w_count = w_count + 1
            if (all(x == 'b' for x in checkList)):
                b_count = b_count + 1
            checkList = []
    
    # check vertically
    checkList = []
    
    for c in range (0, 6):
        for r in range (0, 2):
            checkList.append(state[r][c])
            checkList.append(state[r + 1][c])
            checkList.append(state[r + 2][c])
            checkList.append(state[r + 3][c])
            checkList.append(state[r + 4][c])
            if (all(x == 'w' for x in checkList)):
                w_count = w_count + 1
            if (all(x == 'b' for x in checkList)):
                b_count = b_count + 1
            checkList = []  
     
    # check diagonally 
    for r in range (0, 2):
        for c in range (0, 2): 
            checkList.append(state[r][c])
            checkList.append(state[r + 1][c + 1])
            checkList.append(state[r + 2][c + 2])
            checkList.append(state[r + 3][c + 3])
            checkList.append(state[r + 4][c + 4])
            if (all(x == 'w' for x in checkList)):
                w_count = w_count + 1
            if (all(x == 'b' for x in checkList)):
                b_count = b_count + 1
            checkList = []
            
    checkList = []
    for r in range (4, 6):
        for c in range (0, 2): 
            checkList.append(state[r][c])
            checkList.append(state[r - 1][c + 1])
            checkList.append(state[r - 2][c + 2])
            checkList.append(state[r - 3][c + 3])
            checkList.append(state[r - 4][c + 4])
            if (all(x == 'w' for x in checkList)):
                w_count = w_count + 1
            if (all(x == 'b' for x in checkList)):
                b_count = b_count + 1
            checkList = []
    
                
    # return sum of success lines of 'w' and 'b'
    return [w_count, b_count]


# Check if the block/position is available
def isPositionAvailable(gameBoard, block, position):
    row = (block / 2 * 3) + position / 3
    col = (block % 2 * 3) + position % 3
    
    # check if the place is empty
    if (gameBoard[row][col] == '.'):
        return True
    
    return False


# Rotate the game board
def rotateBoard(gameBoard, rotateBlock, rotateDirection):
    
    rotateBlock = rotateBlock - 1
    
    r = (rotateBlock / 2) * 3
    c = (rotateBlock % 2) * 3
    
    # rotate to left
    if (rotateDirection.lower() == 'l'):
        temp = gameBoard[r][c]
        gameBoard[r][c] = gameBoard[r][c + 2]
        gameBoard[r][c + 2] = gameBoard[r + 2][c + 2] 
        gameBoard[r + 2][c + 2] = gameBoard[r + 2][c]
        gameBoard[r + 2][c] = temp
        
        temp = gameBoard[r][c + 1]
        gameBoard[r][c + 1] = gameBoard[r + 1][c + 2]
        gameBoard[r + 1][c + 2] = gameBoard[r + 2][c + 1] 
        gameBoard[r + 2][c + 1] = gameBoard[r + 1][c]
        gameBoard[r + 1][c] = temp
        
        
    # rotate to right
    elif (rotateDirection.lower() == 'r'):
        temp = gameBoard[r][c]
        gameBoard[r][c] = gameBoard[r + 2][c]
        gameBoard[r + 2][c] = gameBoard[r + 2][c + 2] 
        gameBoard[r + 2][c + 2] = gameBoard[r][c + 2]
        gameBoard[r][c + 2] = temp
        
        temp = gameBoard[r][c + 1]
        gameBoard[r][c + 1] = gameBoard[r + 1][c]
        gameBoard[r + 1][c] = gameBoard[r + 2][c + 1] 
        gameBoard[r + 2][c + 1] = gameBoard[r + 1][c + 2]
        gameBoard[r + 1][c + 2] = temp
        
    return gameBoard


# Check if the input token place and rotation is valid  
def isValidPlace(inputPlace):
    
    if (inputPlace == None or len(inputPlace) != 6):
        print ("Enter valid input (ex: 2/4 1R)" )
        return False
    
    if (inputPlace[0].isdigit()):
        block = int(inputPlace[0])
    else:
        print("Block number should be integer")
        return False
    
    if (inputPlace[2].isdigit()):
        position = int(inputPlace[2])
    else:
        print("Position number should be integer")
        return False    
    
    if (inputPlace[4].isdigit()):
        rotateBlock = int(inputPlace[4])
    else:
        print("Rotated block number should be integer")
        return False  
    
    rotateDirection = inputPlace[5]
    
    if (block not in range (1, 5)):
        print ("Block number should be one of these: 1, 2, 3 or 4")
        return False
    
    if (position not in range (1, 10)):
        print ("Position number should be between 1 and 9")
        return False
        
    if (rotateBlock not in range (1, 5)):
        print ("Rotated Block number should be one of these: 1, 2, 3 or 4")
        return False
    
    if (rotateDirection.lower() != 'r' and rotateDirection.lower() != 'l'):
        print ("Rotate letter should be one of these: R, r, L or l")
        return False
    
    return True    
    
                 
                 
# Display the given game board
def displayBoard(gameBoard):
    board_str = ""
    
    board_str += "+-------+-------+\n"
    for r in range (0, 6):
        row = '| ' + str(gameBoard[r][0])
        for c in range (1, 6):
            if (c == 3):
                row = row + ' | ' + str(gameBoard[r][c])
            else:
                row = row + ' ' + str(gameBoard[r][c])
        if (r == 3):
            board_str += "+-------+-------+\n"
        board_str += (row + ' |\n')
    board_str += "+-------+-------+\n"
    
    return board_str
    
    
# Display numbered board for help
def displayNumberedBoard():
    
    print ("\n\n[Board Blocks and positions]: \n")
    print ("\t      +-------+-------+")
    print ("\tGame  | 1 2 3 | 1 2 3 |  Game")
    print ("\tBlock | 4 5 6 | 4 5 6 |  Block")
    print ("\t  1   | 7 8 9 | 7 8 9 |    2")
    print ("\t      +-------+-------+")
    print ("\tGame  | 1 2 3 | 1 2 3 |  Game")
    print ("\tBlock | 4 5 6 | 4 5 6 |  Block")
    print ("\t  3   | 7 8 9 | 7 8 9 |    4")
    print ("\t      +-------+-------+")






# Node class
class Node:
    def __init__(self):
        self.data = None
        self.depth = 0
        self.children = []
        self.place = None
        self.value = None
         
    def __str__(self):
        return self.data


# Player class    
class Player:
    def __init__(self):
        self.isFirst = False
        self.isBot = False
        self.name = None
        self.token = ''
        
    def __str__(self):
        return self.token
    
    
    
    
    

if __name__ == '__main__':
    main()