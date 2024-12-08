class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject

    def computerHard(self, grid, depth, alpha, beta, player):
        """
        Minimax with Alpha-Beta Pruning for optimal move selection.
        """
        availMoves = self.grid.findAvailMoves(grid, player)
        if depth == 0 or not availMoves:
            return None, self.calculateTileScore(grid, player)

        bestMove = None
        bestScore = float('-inf') if player < 0 else float('inf')

        for move in availMoves:
            x, y = move
            swappableTiles = self.grid.swappableTiles(x, y, grid, player)

            # Simulate the move
            self.makeMove(grid, x, y, swappableTiles, player)
            _, score = self.computerHard(grid, depth - 1, alpha, beta, -player)
            self.undoMove(grid, x, y, swappableTiles, player)

            score += len(swappableTiles) if player < 0 else -len(swappableTiles)

            # Update best score and move
            if player < 0:  # Maximizing player
                if score > bestScore:
                    bestScore = score
                    bestMove = move
                alpha = max(alpha, bestScore)
            else:  # Minimizing player
                if score < bestScore:
                    bestScore = score
                    bestMove = move
                beta = min(beta, bestScore)

            if beta <= alpha:
                break

        return bestMove, bestScore

    def calculateTileScore(self, grid, player):
        return sum(row.count(player) for row in grid) - sum(row.count(-player) for row in grid)

    def makeMove(self, grid, x, y, swappableTiles, player):
        grid[x][y] = player
        for tile in swappableTiles:
            grid[tile[0]][tile[1]] = player

    def undoMove(self, grid, x, y, swappableTiles, player):
        grid[x][y] = 0
        for tile in swappableTiles:
            grid[tile[0]][tile[1]] = -player
