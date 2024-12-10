class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject
        # Positional weights for each grid position to guide AI's move choices
        self.positional_weights = [
            [100, -20, 10, 5, 5, 10, -20, 100],  # Corners are highly weighted
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, 0, 0, 0, 0, -2, 10],
            [5, -2, 0, 0, 0, 0, -2, 5],
            [5, -2, 0, 0, 0, 0, -2, 5],
            [10, -2, 0, 0, 0, 0, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ]


    def computerHard(self, grid, depth, alpha, beta, player):
        availMoves = self.grid.findAvailMoves(grid, player)  # Get available moves
        if depth == 0 or not availMoves:  # Base case: end recursion if no moves or max depth
            return None, self.combinedHeuristic(grid, player)  # Evaluate board state

        bestMove = None
        bestScore = float('-inf') if player < 0 else float('inf')  # Initialize best score

        for move in availMoves:
            x, y = move
            swappableTiles = self.grid.swappableTiles(x, y, grid, player)  # Get swappable tiles
            
            # Simulate the move
            self.makeMove(grid, x, y, swappableTiles, player)  
            _, score = self.computerHard(grid, depth - 1, alpha, beta, -player)  
            self.undoMove(grid, x, y, swappableTiles, player)  
            
            score += len(swappableTiles) if player < 0 else -len(swappableTiles)  
            # Maximize or minimize the score based on the player's turn
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

            if beta <= alpha:  # Prune the search tree if no better move is found
                break

        return bestMove, bestScore

    def calculateTileScore(self, grid, player):
        score = 0
        opponent = -player

        # Sum up scores based on positional weights for each player's tiles
        for x in range(8):
            for y in range(8):
                if grid[x][y] == player:
                    score += self.positional_weights[x][y]  
                elif grid[x][y] == opponent:
                    score -= self.positional_weights[x][y]  

        return score

    def makeMove(self, grid, x, y, swappableTiles, player):
        grid[x][y] = player  # Place the player's piece on the board
        for tile in swappableTiles:
            grid[tile[0]][tile[1]] = player  # Flip opponent's pieces

    def undoMove(self, grid, x, y, swappableTiles, player):
        grid[x][y] = 0  # Remove the player's piece
        for tile in swappableTiles:
            grid[tile[0]][tile[1]] = -player  # Flip opponent's pieces back

    def calculateMobility(self, grid, player):
        # Calculate the difference in available moves between the player and opponent
        return len(self.grid.findAvailMoves(grid, player)) - len(self.grid.findAvailMoves(grid, -player))

    def calculateStability(self, grid, player):
        stabilityScore = 0
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]  # Define corner positions

        # Check if corners are controlled by the player or opponent
        for x, y in corners:
            if grid[x][y] == player:
                stabilityScore += 50  # Add points for controlling corners
            elif grid[x][y] == -player:
                stabilityScore -= 50  # Subtract points for opponent controlling corners
        return stabilityScore

    def combinedHeuristic(self, grid, player):
        # Combine positional score, mobility score, and stability score to evaluate the board
        positionScore = self.calculateTileScore(grid, player)
        mobilityScore = self.calculateMobility(grid, player)
        stabilityScore = self.calculateStability(grid, player)
        return positionScore + 10 * mobilityScore + 5 * stabilityScore  # Weigh each score component
