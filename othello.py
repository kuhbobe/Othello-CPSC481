import pygame
from player import Grid
from computerai import ComputerPlayer

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Othello')
        self.font = pygame.font.SysFont('Arial', 30, True, False)
        
        self.player1 = 1
        self.player2 = -1
        self.currentPlayer = self.player1
        self.time = 0
        self.rows, self.columns = 8, 8
        self.gameOver = False
        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.computerPlayer = ComputerPlayer(self.grid)
        self.RUN = True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseEvent(event)

    def mouseEvent(self, event):
        if event.button == 3:
            self.grid.printGameLogicBoard()
        elif event.button == 1:
            if self.currentPlayer == self.player1 and not self.gameOver:
                self.playerMove()
            elif self.gameOver:
                self.newGame(event)

    def playerMove(self):
        x, y = pygame.mouse.get_pos()
        x, y = (x - 80) // 80, (y - 80) // 80
        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer)
        
        if (y, x) in validCells:
            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, y, x)
            self.tokenFlip(y, x)
            self.currentPlayer *= -1
            self.time = pygame.time.get_ticks()

    def tokenFlip(self, y, x):
        swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayer)
        for tile in swappableTiles:
            self.grid.animateTransitions(tile, self.currentPlayer)
            self.grid.gridLogic[tile[0]][tile[1]] *= -1

    def newGame(self, event):
        x, y = pygame.mouse.get_pos()
        if 320 <= x <= 480 and 400 <= y <= 480:
            self.grid.newGame()
            self.gameOver = False

    def update(self):
        if self.currentPlayer == self.player2:
            self.aiMove()

        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)

        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
            self.gameOver = True

    def aiMove(self):
        difficulty = 5
        new_time = pygame.time.get_ticks()
        if new_time - self.time >= 100:
            if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayer):
                self.gameOver = True
                return
            
            pygame.display.update()  
            # Render "AI is thinking..." message
            self.aiTextDisplay()

            # AI's move logic and Insert token at the AI's chosen position
            cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, difficulty, -64, 64, self.player2)
            self.grid.insertToken(self.grid.gridLogic, self.currentPlayer, cell[0], cell[1])
            self.tokenFlip(cell[0], cell[1])
            # Switch to the next player after AI's move
            self.currentPlayer *= -1
            self.time = pygame.time.get_ticks()
            # Set flag to indicate AI is done thinking
            pygame.display.update()  

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)
        pygame.display.update()

    def aiTextDisplay(self):
        thinking_text = self.font.render('AI is thinking...', True, (255, 255, 255))
        self.screen.blit(thinking_text, (320, 740))  # Position of the message on the screen
        pygame.display.update()  
