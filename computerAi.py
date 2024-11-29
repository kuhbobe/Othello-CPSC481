# ComputerAI.py
import copy

class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject

    def computerHard(self, grid, depth, alpha, beta, player):
        availMoves = self.grid.findAvailMoves(grid, player)

        if depth == 0 or not availMoves:
            return None, self.calculateTileScore(grid, player)

        bestMove = None
        if player < 0:
            bestScore = -64
        else:
            bestScore = 64

        for move in availMoves:
            x, y = move
            swappableTiles = self.grid.swappableTiles(x, y, grid, player)
            flippedCount = len(swappableTiles)  # Count tiles flipped for scoring

            # Make the move
            grid[x][y] = player
            for tile in swappableTiles:
                grid[tile[0]][tile[1]] = player

            # Recursively evaluate the move
            _, score = self.computerHard(grid, depth - 1, alpha, beta, -player)

            # Add flippedCount to the score (heuristic-based scoring)
            if player < 0:
                score += flippedCount
            else:
                score -= flippedCount

            # Undo the move
            grid[x][y] = 0
            for tile in swappableTiles:
                grid[tile[0]][tile[1]] = -player

            # Update the best score and move
            if player < 0:
                if score > bestScore:
                    bestScore = score
                    bestMove = move
                alpha = max(alpha, bestScore)
            else:
                if score < bestScore:
                    bestScore = score
                    bestMove = move
                beta = min(beta, bestScore)

            # Alpha-beta pruning
            if beta <= alpha:
                break

        return bestMove, bestScore

    def calculateTileScore(self, grid, player):
        playerTiles = sum(row.count(player) for row in grid)
        opponentTiles = sum(row.count(-player) for row in grid)
        return playerTiles - opponentTiles

