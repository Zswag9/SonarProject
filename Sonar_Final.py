# Sonar

class player:
    def __init__(self):
        self.sonar = 16

    @staticmethod
    def getRow(board, row):
        # Return a string from the board data structure at a certain row.
        boardRow = ''
        for i in range(60):
            boardRow += board[i][row]
        return boardRow

    @staticmethod
    def getNewBoard():
        # Create a new 60x15 board data structure.
        board = []
        for x in range(60):  # the main list is a list of 60 lists
            board.append([])
            for y in range(15):  # each list in the main list has 15 single-character strings
                # use different characters for the ocean to make it more readable.
                if random.randint(0, 1) == 0:
                    board[x].append('~')
                else:
                    board[x].append('`')
        return board

    def enterPlayerMove(whichPlayer):
        # Let the player type in her move. Return a two-item list of int xy coordinates.
        if whichPlayer == 0 or whichPlayer == 2 or whichPlayer == 4 or whichPlayer == 6 or whichPlayer == 8 or whichPlayer == 10 or whichPlayer == 12 or whichPlayer == 14 or whichPlayer == 16:
            print('It\'s Player One\'s turn!')
        else:
            print('It\'s Player Two\'s turn!')
        print('Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)')
        while True:
            move = input()
            if move.lower() == 'quit':
                print('Thanks for playing!')
                sys.exit()

            move = move.split()
            if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and player.isValidMove(int(move[0]),
                                                                                                 int(move[1])):
                return [int(move[0]), int(move[1])]
            print('Enter a number from 0 to 59, a space, then a number from 0 to 14.')

    def drawBoard(board):
        # Draw the board data structure.

        hline = '    '  # initial space for the numbers down the left side of the board
        for i in range(1, 6):
            hline += (' ' * 9) + str(i)

        # print the numbers across the top
        print(hline)
        print('   ' + ('0123456789' * 6))
        print()

        # print each of the 15 rows
        for i in range(15):
            # single-digit numbers need to be padded with an extra space
            if i < 10:
                extraSpace = ' '
            else:
                extraSpace = ''
            print('%s%s %s %s' % (extraSpace, i, player.getRow(board, i), i))
        # print the numbers across the bottom
        print()
        print('   ' + ('0123456789' * 6))
        print(hline)

    def makeMove(board, chests, x, y):
        # Change the board data structure with a sonar device character. Remove treasure chests
        # from the chests list as they are found. Return False if this is an invalid move.
        # Otherwise, return the string of the result of this move.
        if not player.isValidMove(x, y):
            return False

        smallestDistance = 100  # any chest will be closer than 100.
        for cx, cy in chests:
            if abs(cx - x) > abs(cy - y):
                distance = abs(cx - x)
            else:
                distance = abs(cy - y)

            if distance < smallestDistance:  # we want the closest treasure chest.
                smallestDistance = distance

        if smallestDistance == 0:
            # xy is directly on a treasure chest!
            chests.remove([x, y])
            return 'You have found a sunken treasure chest!'
        else:
            if smallestDistance < 10:
                board[x][y] = str(smallestDistance)
                return 'Treasure detected at a distance of %s from the sonar device.' % (smallestDistance)
            else:
                board[x][y] = 'O'
                return 'Sonar did not detect anything. All treasure chests out of range.'

    def isValidMove(x, y):
        # Return True if the coordinates are on the board, otherwise False.
        return x >= 0 and x <= 59 and y >= 0 and y <= 14

    def getRandomChests(numChests):
        # Create a list of chest data structures (two-item lists of x, y int coordinates)
        chests = []
        for i in range(numChests):
            chests.append([random.randint(0, 59), random.randint(0, 14)])
        return chests

    def playAgain():
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')


import random
import sys

P1 = player()
P2 = player()


def showInstructions():
    print('''Instructions:
You are the captain of the Simon, a treasure-hunting ship. Your current mission
is to find the three sunken treasure chests that are lurking in the part of the
ocean you are in and collect them.
To play, enter the coordinates of the point in the ocean you wish to drop a
sonar device. The sonar can find out how far away the closest chest is to it.
For example, the d below marks where the device was dropped, and the 2's
represent distances of 2 away from the device. The 4's represent
distances of 4 away from the device.
    444444444
    4       4
    4 22222 4
    4 2   2 4
    4 2 d 2 4
    4 2   2 4
    4 22222 4
    4       4
    444444444
Press enter to continue...''')
    input()

    print('''For example, here is a treasure chest (the c) located a distance of 2 away
from the sonar device (the d):
    22222
    c   2
    2 d 2
    2   2
    22222
The point where the device was dropped will be marked with a 2.
The treasure chests don't move around. Sonar devices can detect treasure
chests up to a distance of 9. If all chests are out of range, the point
will be marked with O
If a device is directly dropped on a treasure chest, you have discovered
the location of the chest, and it will be collected. The sonar device will
remain there.
When you collect a chest, all sonar devices will update to locate the next
closest sunken treasure chest.
Press enter to continue...''')
    input()
    print()


print('S O N A R !')
print()
print('Would you like to view the instructions? (yes/no)')
if input().lower().startswith('y'):
    showInstructions()

while True:
    # game setup
    P1 = player()
    P2 = player()
    sonarDevices = P1.sonar + P2.sonar
    p = 0
    theBoard = player.getNewBoard()
    theChests = player.getRandomChests(3)
    player.drawBoard(theBoard)
    previousMoves = []
    turn = random.randint(0, 1)

    while sonarDevices > 0:
        # Start of a turn:

        # sonar device/chest status
        if P1.sonar > 1 and P2.sonar > 1:
            extraSsonar = 's'
        else:
            extraSsonar = ''
        if len(theChests) > 1:
            extraSchest = 's'
        else:
            extraSchest = ''
        if p % 2 == 1:
            print('You have %s sonar device%s left. %s treasure chest%s remaining.' % (
            P1.sonar, extraSsonar, len(theChests), extraSchest))
        else:
            print('You have %s sonar device%s left. %s treasure chest%s remaining.' % (
            P2.sonar, extraSsonar, len(theChests), extraSchest))

        turn = turn + 1

        x, y = player.enterPlayerMove(turn)
        previousMoves.append([x, y])  # we must track all moves so that sonar devices can be updated.

        moveResult = player.makeMove(theBoard, theChests, x, y)
        if moveResult == False:
            continue
        else:
            if moveResult == 'You have found a sunken treasure chest!':
                # update all the sonar devices currently on the map.
                for x, y in previousMoves:
                    player.makeMove(theBoard, theChests, x, y)
            player.drawBoard(theBoard)
            print(moveResult)
            p += 1

        if len(theChests) == 0:
            print('You have found all the sunken treasure chests! Congratulations and good game!')
            break
        if p % 2 == 1:
            P1.sonar -= 1
        else:
            P2.sonar -= 1

        if P1.sonar == 0 and P2.sonar == 0:
            print('We\'ve run out of sonar devices! Now we have to turn the ship around and head')
            print('for home with treasure chests still out there! Game over.')
            print('    The remaining chests were here:')
            for x, y in theChests:
                print('    %s, %s' % (x, y))
            break

    if not player.playAgain():
        sys.exit()