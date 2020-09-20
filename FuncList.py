import Tkinter
from Tkinter import *
from SoldierClass import CheckerSoldier

class CheckerBoard(Canvas):
    # CONSTANTS
    WHITE_SOLDIER = 1
    BLACK_SOLDIER = 2

    # Soldiers
    whiteSoldiers = []
    blackSoldiers = []

    # GAMEBOARD (8X8 TILES)
    gb = Tkinter.Tk()
    board = []
    highlightedTiles = []
    currentlySelectedCheckerObject = CheckerSoldier(0, 0, "white", False, 0)
    currentlySelectedCheckerID = 0
    tileWidth = 31.5
    tileHeight = 31.5
    rows = 8
    columns = 8
    tileBorder = .5
    checkerBorder = 4
    currentPlayer = "black"
    mustDoubleJump = False
    blackCount = 12
    whiteCount = 12
    blackScoreBoard = Label(gb, text="Black: %i" % blackCount)
    whiteScoreBoard = Label(gb, text="White: %i" % whiteCount)

    # RESETS GAMEBOARD, PLACES ALL SOLDIERS IN ORIGINAL POSITIONS (NEWGAME)
    def startNewGame(self):
        # REMOVE ALL SOLDIERS FROM THE BOARD
        for i in self.whiteSoldiers:
            self.delete(i[0])
        for i in self.blackSoldiers:
            self.delete(i[0])

        # CLEAR ALL DATA FROM THE ARRAYS
        for i in range(0, len(self.whiteSoldiers)):
            self.whiteSoldiers.pop()

        for i in range(0, len(self.blackSoldiers)):
            self.blackSoldiers.pop()

        for i in range(0, len(self.highlightedTiles)):
            self.highlightedTiles.pop()

        # RESET ALL VARIABLES TO ORIGINAL VALUES
        self.whiteSoldiers = []
        self.blackSoldiers = []
        self.highlightedTiles = []
        self.currentlySelectedCheckerObject = CheckerSoldier(0, 0, "white", False, 0)
        self.currentlySelectedCheckerID = 0
        self.currentPlayer = "black"
        self.mustDoubleJump = False
        self.blackCount = 12
        self.whiteCount = 12
        self.blackScoreBoard.config(text="Black: %i" % self.blackCount)
        self.whiteScoreBoard.config(text="White: %i" % self.whiteCount)

        # CREATE NEW SOLDIERS
        self.createCheckers()

    # __init__ INITIALIZES THE MAIN WINDOW, GAMEBOARD, CANVAS, AND SOLDIERS
    def __init__(self):
        self.gb.minsize(500, 400)
        Canvas.__init__(self, self.gb, bg="black", height=250, width=250)
        newGameButton = Button(self.gb, text="New Game", command=self.startNewGame)
        self.blackScoreBoard.pack()
        self.whiteScoreBoard.pack()
        self.pack()
        newGameButton.pack()
        self.createTiles()

        self.createCheckers()

        self.gb.resizable(False,False)
        screen_width = self.gb.winfo_screenwidth()
        screen_height = self.gb.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (250 / 2))
        y_cordinate = int((screen_height / 2) - (200 / 2))

        self.gb.geometry("{}x{}+{}+{}".format(250, 200, x_cordinate, y_cordinate))
        self.gb.mainloop()

    # CREATES TILES
    def createTiles(self):
        width = self.tileWidth
        height = self.tileHeight
        for i in range(0, self.columns):
            x1 = (i * width) + self.tileBorder
            x2 = ((i + 1) * width) - self.tileBorder
            for j in range(0, self.rows):
                y1 = (j * height) + self.tileBorder
                y2 = ((j + 1) * height) - self.tileBorder
                idVal = 0
                if ((i + j) % 2 == 0):
                    idVal = self.create_rectangle(x1, y1, x2, y2, fill="#FF9D47")
                else:
                    idVal = self.create_rectangle(x1, y1, x2, y2, fill="#3F2D13")
                if idVal != 0:
                    self.board.append((idVal, j, i, x1, x2, y1, y2))

    # PLACES ALL SOLDIERS ON THE GAMEBOARD IN THEIR CORRECT POSITIONS
    def createCheckers(self):
        checkerWidth = self.tileWidth
        checkerHeight = self.tileWidth
        # ITERATE THROUGH THE ROWS TO PLACE THE SOLDIERS
        for i in range(0, self.rows):
            # DOESNT ALLOW SOLDIERS TO BE PLACED IN ROWS 3 AND 4
            if i == 3 or i == 4:
                continue
            y1 = (i * checkerWidth) + self.checkerBorder
            y2 = ((i + 1) * checkerWidth) - self.checkerBorder
            # WHITE SOLDIERS ARE PLACED IN ROWS 0-2
            if i < 3:
                checkerColor = "white"
            # BLACK SOLDIERS ARE PLACED IN ROWS 5-7
            elif i > 4:
                checkerColor = "black"
            # ITERATE THROUGH THE COLUMNS TO PLACE THE SOLDIERS
            for j in range(0, self.columns):
                # IF I + J = AN ODD NUMBER A SOLDIER WILL BE PLACED IN THAT SQUARE
                if ((i + j) % 2 == 1):
                    x1 = (j * checkerHeight) + self.checkerBorder
                    x2 = ((j + 1) * checkerHeight) - self.checkerBorder
                    # PLACE THE SOLDIER ON THE BOARD, GIVES IT A COLOR AND ID
                    idTag = self.create_oval(x1, y1, x2, y2, fill=checkerColor)
                    self.tag_bind(idTag, "<ButtonPress-1>", self.processCheckerClick)
                    # Create a soldier object to keep track of this newly created soldier
                    newChecker = CheckerSoldier(i, j, checkerColor, False, idTag)
                    # Append the id and checker object to their proper arrays
                    if checkerColor == "white":
                        self.whiteSoldiers.append((idTag, newChecker))
                    elif checkerColor == "black":
                        self.blackSoldiers.append((idTag, newChecker))

    # DETECTS WHEN A USER CLICKS A SOLDIER
    def processCheckerClick(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        idValue = self.find_closest(x, y)[0]
        selectedChecker = self.getCheckerObject(idValue)
        # IF THE SELECTED SOLDIER HAS AN ID VALUE OF 0 IT DOES NOT EXIST
        if selectedChecker == 0:
            return
        # ONLY PROCESS THE CLICK IF THE SELECTED SOLDIER IS THE PROPER COLOR BASED ON TURNS
        if (self.currentPlayer == selectedChecker.getColor()) and (self.mustDoubleJump == False):
            # RETRIEVE THE CURRENTLY SELECTED SOLDIER'S ID AND COLOR
            self.currentlySelectedCheckerObject = selectedChecker
            self.currentlySelectedCheckerID = idValue
            # RESET ALL SELECTED TILES
            self.resetHighlightedTiles()
            # HIGHLIGHTS POSSIBLE TILES THE PLAYER CAN MOVE THE SOLDIER TO
            self.showAllAvailableRegularMoves(selectedChecker)
            # SHOWS ALL THE JUMPS THAT ARE AVAILABLE FOR THAT SOLDIER
            self.showAllAvailableJumpMoves(selectedChecker)

    # PROCESSES MOVEMENT OF SOLDIERS
    def processHighlightedTileClicked(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        idValue = self.find_closest(x, y)[0]
        # FIND THE ROW AND COLUMN OF WHERE THE SOLDIER IS MOVING TO
        newRow = 100
        newCol = 100
        jumpedCheckerID = 0
        for i in self.board:
            if i[0] == idValue:
                newRow = i[1]
                newCol = i[2]
                jumpedCheckerID = self.getJumpedCheckerID(newRow, newCol)
                break
        if newRow == 100:
            return

        # MOVE THE SOLDIER TO THE SELECTED POSITION IF IT IS VALID
        self.moveCurrentlySelectedChecker(newRow, newCol)
        self.resetHighlightedTiles()
        # IF THAT MOVE WAS A JUMP REMOVE THE jumpSOLDIER
        if jumpedCheckerID != 0:
            self.removeChecker(jumpedCheckerID)
            self.showAllAvailableJumpMoves(self.currentlySelectedCheckerObject)
            # If there are jumps left for the player, set the mustDoubleJump flag to true
            if len(self.highlightedTiles) > 0:
                self.mustDoubleJump = True
            # Else if there are no jumps left for the player, set the mustDoubleJump flag to false and switch players
            else:
                self.switchCurrentPlayer()
                self.mustDoubleJump = False
        # If the selected checker was just a normal move, switch players
        else:
            self.switchCurrentPlayer()

    # Description: Switch the current player to the next player
    def switchCurrentPlayer(self):
        if self.currentPlayer == "black":
            self.currentPlayer = "white"
        elif self.currentPlayer == "white":
            self.currentPlayer = "black"

    # Description: Remove soldier from the board and its respective soldier array
    def removeChecker(self, checkerID):
        if checkerID != 0:
            self.delete(checkerID)
            for i in self.blackSoldiers:
                if i[0] == checkerID:
                    self.blackSoldiers.remove(i)
                    self.blackCount = self.blackCount - 1
                    self.blackScoreBoard.config(text="Black: %i" % self.blackCount)
                    break
            for i in self.whiteSoldiers:
                if i[0] == checkerID:
                    self.whiteSoldiers.remove(i)
                    self.whiteCount = self.whiteCount - 1
                    self.whiteScoreBoard.config(text="White: %i" % self.whiteCount)
                    break
            self.checkForWin()

    # Description: Check if black or white has won. If so, congratulate them
    def checkForWin(self):
        if self.blackCount <= 0:
            whiteWinnerLabel = Label(self.gb, text="White Wins!")
            whiteWinnerLabel.pack()
            self.stopTheGame()
        elif self.whiteCount <= 0:
            blackWinnerLabel = Label(self.gb, text="Black Wins!")
            blackWinnerLabel.pack()
            self.stopTheGame()

    # Description: Stops the game by unbinding all events
    def stopTheGame(self):
        for i in self.blackSoldiers:
            checkerIDVal = i[0]
            if checkerIDVal != 0:
                self.tag_unbind(checkerIDVal, "<ButtonPress-1>")
        for i in self.whiteSoldiers:
            checkerIDVal = i[0]
            if checkerIDVal != 0:
                self.tag_unbind(checkerIDVal, "<ButtonPress-1>")
        self.resetHighlightedTiles()

    # Description: given row and column, get jumped soldier id
    def getJumpedCheckerID(self, row_, col_):
        for i in self.highlightedTiles:
            if row_ == i[0] and col_ == i[1]:
                return i[2]
        return 0

    # Description: move the currently selected soldier to (newRow_, newCol_)
    def moveCurrentlySelectedChecker(self, newRow_, newCol_):
        y1 = (newRow_ * self.tileWidth) + self.checkerBorder
        y2 = ((newRow_ + 1) * self.tileWidth) - self.checkerBorder
        x1 = (newCol_ * self.tileWidth) + self.checkerBorder
        x2 = ((newCol_ + 1) * self.tileWidth) - self.checkerBorder
        # Move soldier to new location
        self.coords(self.currentlySelectedCheckerID, (x1, y1, x2, y2))
        # Update currentlySelectedSoldier's location
        self.currentlySelectedCheckerObject.updateLocation(newRow_, newCol_)
        if self.currentlySelectedCheckerObject.isKing():
            self.itemconfig(self.currentlySelectedCheckerID, outline="red")

    # Description: reset all highlighted tiles to black borders instead of yellow
    #                unbind all events the highlighted tiles had
    def resetHighlightedTiles(self):
        # Reset all currently highlighted cells
        for i in self.highlightedTiles:
            tileIDVal = self.getTileID(i[0], i[1])
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="black")
                self.tag_unbind(tileIDVal, "<ButtonPress-1>")

        # Remove all current values from highlightedTiles
        for i in range(0, len(self.highlightedTiles)):
            self.highlightedTiles.pop()

    # Description: show available moves for a selected soldier
    def showAllAvailableRegularMoves(self, _selectedChecker):
        selectedChecker = _selectedChecker
        selectedCheckerIsKing = selectedChecker.isKing()
        selectedCheckerColor = selectedChecker.getColor()
        openSpaces = []

        if selectedCheckerIsKing:
            # Check north west neighbor
            rowValue = selectedChecker.getNWneighbor()[0]
            colValue = selectedChecker.getNWneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getNWneighbor())

            # Check north east neighbor
            rowValue = selectedChecker.getNEneighbor()[0]
            colValue = selectedChecker.getNEneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getNEneighbor())

            # Check south west neighbor
            rowValue = selectedChecker.getSWneighbor()[0]
            colValue = selectedChecker.getSWneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getSWneighbor())

            # Check south east neighbor
            rowValue = selectedChecker.getSEneighbor()[0]
            colValue = selectedChecker.getSEneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getSEneighbor())
        # Else if soldier is normal and black, only check north west and north east
        elif selectedCheckerColor == "black":
            # Check north west neighbor
            rowValue = selectedChecker.getNWneighbor()[0]
            colValue = selectedChecker.getNWneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getNWneighbor())

            # Check north east neighbor
            rowValue = selectedChecker.getNEneighbor()[0]
            colValue = selectedChecker.getNEneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getNEneighbor())
        # Else if soldier is normal and white, only check south west and south east
        elif selectedCheckerColor == "white":
            # Check south west neighbor
            rowValue = selectedChecker.getSWneighbor()[0]
            colValue = selectedChecker.getSWneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getSWneighbor())

            # Check south east neighbor
            rowValue = selectedChecker.getSEneighbor()[0]
            colValue = selectedChecker.getSEneighbor()[1]
            if (not self.isTileOccupied(rowValue, colValue)[0]):
                openSpaces.append(selectedChecker.getSEneighbor())

        # Highlight all open spaces
        for i in range(0, len(openSpaces)):
            highlightRow = openSpaces[i][0]
            highlightCol = openSpaces[i][1]
            if highlightRow == 100 or highlightCol == 100:
                continue
            tileIDVal = self.getTileID(highlightRow, highlightCol)
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="yellow")
                self.tag_bind(tileIDVal, "<ButtonPress-1>", self.processHighlightedTileClicked)
                self.highlightedTiles.append((highlightRow, highlightCol, 0))
            else:
                print "Invalid tile"

    # Description: Show all available jump moves a selected soldier can make
    def showAllAvailableJumpMoves(self, selectedChecker_):
        selectedChecker = selectedChecker_
        selectedCheckerIsKing = selectedChecker.isKing()
        selectedCheckerColor = selectedChecker.getColor()

        if selectedCheckerIsKing:
            # Check north west neighbor
            rowValue = selectedChecker.getNWneighbor()[0]
            colValue = selectedChecker.getNWneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getNWneighbor()[0]
                    jumpCol = selectedChecker.getNWneighbor()[1]
                    self.checkForJump(jumpRow - 1, jumpCol - 1, jumpCheckerID)

            # Check north east neighbor
            rowValue = selectedChecker.getNEneighbor()[0]
            colValue = selectedChecker.getNEneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getNEneighbor()[0]
                    jumpCol = selectedChecker.getNEneighbor()[1]
                    self.checkForJump(jumpRow - 1, jumpCol + 1, jumpCheckerID)

            # Check south west neighbor
            rowValue = selectedChecker.getSWneighbor()[0]
            colValue = selectedChecker.getSWneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getSWneighbor()[0]
                    jumpCol = selectedChecker.getSWneighbor()[1]
                    self.checkForJump(jumpRow + 1, jumpCol - 1, jumpCheckerID)

            # Check south east neighbor
            rowValue = selectedChecker.getSEneighbor()[0]
            colValue = selectedChecker.getSEneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getSEneighbor()[0]
                    jumpCol = selectedChecker.getSEneighbor()[1]
                    self.checkForJump(jumpRow + 1, jumpCol + 1, jumpCheckerID)

        # Else if soldier is a normal and black check the north west and north east neighbors
        elif selectedCheckerColor == "black":
            # Check north west neighbor
            rowValue = selectedChecker.getNWneighbor()[0]
            colValue = selectedChecker.getNWneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getNWneighbor()[0]
                    jumpCol = selectedChecker.getNWneighbor()[1]
                    self.checkForJump(jumpRow - 1, jumpCol - 1, jumpCheckerID)

            # Check north east neighbor
            rowValue = selectedChecker.getNEneighbor()[0]
            colValue = selectedChecker.getNEneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getNEneighbor()[0]
                    jumpCol = selectedChecker.getNEneighbor()[1]
                    self.checkForJump(jumpRow - 1, jumpCol + 1, jumpCheckerID)

        elif selectedCheckerColor == "white":
            # Check south west neighbor
            rowValue = selectedChecker.getSWneighbor()[0]
            colValue = selectedChecker.getSWneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getSWneighbor()[0]
                    jumpCol = selectedChecker.getSWneighbor()[1]
                    self.checkForJump(jumpRow + 1, jumpCol - 1, jumpCheckerID)

            # Check south east neighbor
            rowValue = selectedChecker.getSEneighbor()[0]
            colValue = selectedChecker.getSEneighbor()[1]
            isTileOccupiedReturnArray = self.isTileOccupied(rowValue, colValue)
            isTileOccupied = isTileOccupiedReturnArray[0]
            tileColor = isTileOccupiedReturnArray[1]
            jumpCheckerID = isTileOccupiedReturnArray[2]
            if isTileOccupied:
                if selectedCheckerColor != tileColor:
                    jumpRow = selectedChecker.getSEneighbor()[0]
                    jumpCol = selectedChecker.getSEneighbor()[1]
                    self.checkForJump(jumpRow + 1, jumpCol + 1, jumpCheckerID)

    # Description: Highlight square if jump tile is not occupied
    def checkForJump(self, row_, col_, jumpedCheckerID_):
        # If row_ and col_ are not on the board, return
        if not self.isValidPosition(row_, col_):
            return 0
        # If tile is not occupied, highlight it
        if not self.isTileOccupied(row_, col_)[0]:
            tileIDVal = self.getTileID(row_, col_)
            if tileIDVal != 0:
                self.itemconfig(tileIDVal, outline="yellow")
                self.tag_bind(tileIDVal, "<ButtonPress-1>", self.processHighlightedTileClicked)
                self.highlightedTiles.append((row_, col_, jumpedCheckerID_))

    # Description: Checks if tile described by the rowVal and colVal is occupied
    #                If occupied, returns (True, <colorOfCheckerOccupyingTheTile> , <idOfCheckerOccupyingTheTile>)
    #                If not occupied, returns (False, "NA", 0)
    def isTileOccupied(self, rowVal, colVal):
        row = rowVal
        col = colVal

        if (not self.isValidPosition(row, col)):
            return (False, "NA", 0)

        # Check if any white soldiers are in the tile
        for i in range(0, len(self.whiteSoldiers)):
            currentChecker = self.whiteSoldiers[i][1]
            if (row == currentChecker.getRow()) and (col == currentChecker.getColumn()):
                return (True, "white", self.whiteSoldiers[i][0])

        # Check if any black soldiers are in the tile
        for i in range(0, len(self.blackSoldiers)):
            currentChecker = self.blackSoldiers[i][1]
            if (row == currentChecker.getRow()) and (col == currentChecker.getColumn()):
                return (True, "black", self.blackSoldiers[i][0])

        # No soldiers found in the tile, return (False, "NA", 0)
        return (False, "NA", 0)

    # Description: returns the soldier object representing the passed id value
    def getCheckerObject(self, idValue):
        # Check whiteSoldiers for id
        for i in range(0, len(self.whiteSoldiers)):
            if self.whiteSoldiers[i][0] == idValue:
                return self.whiteSoldiers[i][1]

        # Check blackSoldiers for id
        for i in range(0, len(self.blackSoldiers)):
            if self.blackSoldiers[i][0] == idValue:
                return self.blackSoldiers[i][1]

        # If no soldier found, return 0
        return 0

    # Description: Return the tileID of the tile found at (row_, col_)
    def getTileID(self, row_, col_):
        row = row_
        col = col_
        for i in range(0, len(self.board)):
            if row == self.board[i][1] and col == self.board[i][2]:
                return self.board[i][0]
        return 0

    # Description: Return true if the position is valid
    def isValidPosition(self, row_, col_):
        return self.isValidRow(row_) and self.isValidColumn(col_)

    # Description: Return true if the row is valid
    def isValidRow(self, row_):
        if (row_ >= 0 and row_ <= 7):
            return True
        else:
            return False

    # Description: Return true if the col is valid
    def isValidColumn(self, col_):
        if (col_ >= 0 and col_ <= 7):
            return True
        else:
            return False


