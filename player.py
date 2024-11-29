# Player.py
import pygame

def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    # Define relative moves for all directions (8 directions)
    moves = [
        (-1, 0),  # Left
        (-1, -1), # Top-left
        (-1, 1),  # Bottom-left
        (1, 0),   # Right
        (1, -1),  # Top-right
        (1, 1),   # Bottom-right
        (0, -1),  # Up
        (0, 1)    # Down
    ]
    
    # Generate valid directions based on boundaries
    return [
        (x + dx, y + dy)
        for dx, dy in moves
        if minX <= x + dx <= maxX and minY <= y + dy <= maxY
    ]

def loadImages(path, size):
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img



def evaluateBoard(grid, player):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            score -= col
    return score

class Token:
    GRID_SIZE = 80  # Grid size in pixels

    def __init__(self, player, gridX, gridY, image, game):
        self.player = player
        self.gridX = gridX
        self.gridY = gridY
        self.image = image
        self.game = game

    @property
    def posX(self):
        return self.GRID_SIZE + (self.gridY * self.GRID_SIZE)

    @property
    def posY(self):
        return self.GRID_SIZE + (self.gridX * self.GRID_SIZE)

    def transition(self, transitionImages, tokenImage, steps=30, frame_step=10):
        for i in range(steps):
            self.image = transitionImages[i // frame_step]
            self.game.draw()  # Assumes `self.game.draw()` handles refreshing the display

        # Set the final image
        self.image = tokenImage

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))

class Grid:
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.y = rows
        self.x = columns
        self.size = size
        # Swap token images here
        self.whitetoken = loadImages('assets/BlackToken.png', size)  # Black token as white
        self.blacktoken = loadImages('assets/WhiteToken.png', size)  # White token as black
        self.bg = self.loadBackGroundImages()
        self.tokens = {}
        self.gridBg = self.createbgimg()
        self.gridLogic = self.regenGrid(self.y, self.x)
        self.player1Score = 0
        self.player2Score = 0
        self.font = pygame.font.SysFont('Arial', 20, True, False)


    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenGrid(self.y, self.x)

    def loadBackGroundImages(self):
        alpha = 'ABCDEFGHI'
        spriteSheet = pygame.image.load('assets/grid.png').convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j] + str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict

    def createbgimg(self):
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = pygame.Surface((960, 960))
        
        # Calculate the positions and blit all images at once (loop optimization)
        for j, row in enumerate(gridBg):
            for i, img_key in enumerate(row):
                # Blit the image using the dictionary
                image.blit(self.bg[img_key], (i * self.size[0], j * self.size[1]))
        
        return image

    def regenGrid(self, rows, columns):
        """generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        textImg = self.font.render(f'{player} : {score}', 1, 'White')
        return textImg

    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            endScreenImg.fill((0, 0, 0))  # Background color

            # Create the text surface
            endText = self.font.render(
                f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1,
                'White'
            )

            # Get the rect of the text
            text_rect = endText.get_rect()

            # Center the text in the middle of the screen
            text_rect.centerx = endScreenImg.get_width() // 2  # Horizontally center
            text_rect.centery = 50  # Set vertical position manually (adjustable)

            # Blit the text onto the end screen
            endScreenImg.blit(endText, text_rect)

            # Draw the "Play Again" button
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')

            # Center the "Play Again" text on the button
            newGameTextRect = newGameText.get_rect(center=(80 + 160 // 2, 160 + 80 // 2))
            endScreenImg.blit(newGameText, newGameTextRect)
        return endScreenImg

    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        window.blit(self.drawScore('Black', self.player1Score), (150, 730))
        window.blit(self.drawScore('White', self.player2Score), (550, 730))

        for token in self.tokens.values():
            token.draw(window)

        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
        if self.GAME.currentPlayer == 1:
            for move in availMoves:
                pygame.draw.circle(window, 'Black', (80 + (move[1] * 80) + 40, 80 + (move[0] * 80) + 40), 30, 2)


        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))

    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.gridLogic):
            line = f'{i} |'.ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + '|'
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:
                        continue

                    validCellToClick.append((gridX, gridY))
        return validCellToClick

    def swappableTiles(self, x, y, grid, player):
        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                checkX += difX
                checkY += difY

                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles

    def findAvailMoves(self, grid, currentPlayer):
        """Takes the list of validCells and checks each to see if playable"""
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            # if len(swapTiles) > 0 and cell not in playableCells:
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells

    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def animateTransitions(self, cell, player):
        """Directly update token image without animation."""
        tokenImage = self.whitetoken if player == 1 else self.blacktoken
        self.tokens[(cell[0], cell[1])].image = tokenImage


def loadSpriteSheet(sheet, row, col, newSize, size):
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey('Black')
    return image