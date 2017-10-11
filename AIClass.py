import math
from PlayerClasses import Player

INFINITY = math.inf
class AI(Player):	
	depth = None
	showScores = False
	def __init__(self, chip='X', difficulty=1, showScores='n'):
		super(AI, self).__init__(chip)
		self.setDifficulty(difficulty)
		self.logScores(showScores)		

	def setDifficulty(self, difficulty):
		self.depth = difficulty

	def logScores(self, showScores):
		if showScores == 'y':
			self.showScores = True

	def playTurn(self, board):
		move = self.miniMax(self.chip, board, self.depth)
		board.addChip(self.chip, move[1], move[2])
		return move[1], move[2]

	def generateMoves(self, board):
		possibleMoves = [] #list of possible positions
		for column in range(board.boardWidth):
			move = board.canAddChip(column)
			if move[0]: #if chip can be added
				possibleMoves.append((move[1], column)) # (row, column)
		return possibleMoves
	

	def evaluateHeuristic(self, board):
		
		horizontalScore = 0
		verticalScore = 0
		diagonal1Score = 0
		diagonal2Score = 0

		'''	// Vertical
		    // Check each column for vertical score
		    // 
		    // 3 pssible situations per column
		    //  0  1  2  3  4  5  6
		    // [x][ ][ ][ ][ ][ ][ ] 0
		    // [x][x][ ][ ][ ][ ][ ] 1
		    // [x][x][x][ ][ ][ ][ ] 2
		    // [x][x][x][ ][ ][ ][ ] 3
		    // [ ][x][x][ ][ ][ ][ ] 4
		    // [ ][ ][x][ ][ ][ ][ ] 5
    	'''

		for row in range(board.boardHeight - 3):
			for column in range(board.boardWidth):
				score = self.scorePosition(board, row, column, 1, 0)
				verticalScore += score

		'''
			// Horizontal
		    // Check each row's score
		    // 
		    // 4 possible situations per row
		    //  0  1  2  3  4  5  6
		    // [x][x][x][x][ ][ ][ ] 0
		    // [ ][x][x][x][x][ ][ ] 1
		    // [ ][ ][x][x][x][x][ ] 2
		    // [ ][ ][ ][x][x][x][x] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
    	'''
		for row in range(board.boardHeight):
			for column in range(board.boardWidth - 3):
				score = self.scorePosition(board, row, column, 0, 1)
				horizontalScore += score

		'''	// Diagonal points 1 (negative-slope)
		    //
		    // 
		    //  0  1  2  3  4  5  6
		    // [x][ ][ ][ ][ ][ ][ ] 0
		    // [ ][x][ ][ ][ ][ ][ ] 1
		    // [ ][ ][x][ ][ ][ ][ ] 2
		    // [ ][ ][ ][x][ ][ ][ ] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
    	'''
		for row in range(board.boardHeight-3):
			for column in range(board.boardWidth - 3):
				score = self.scorePosition(board, row, column, 1, 1)
				diagonal1Score += score

		'''
		    // Diagonal points 2 (positive slope)
		    //
		    // 
		    //  0  1  2  3  4  5  6
		    // [ ][ ][ ][x][ ][ ][ ] 0
		    // [ ][ ][x][ ][ ][ ][ ] 1
		    // [ ][x][ ][ ][ ][ ][ ] 2
		    // [x][ ][ ][ ][ ][ ][ ] 3
		    // [ ][ ][ ][ ][ ][ ][ ] 4
		    // [ ][ ][ ][ ][ ][ ][ ] 5
		'''
		for row in range(3, board.boardHeight):
			for column in range(board.boardWidth - 5):
				score = self.scorePosition(board, row, column, -1, 1)
				diagonal2Score += score

		return horizontalScore + verticalScore + diagonal1Score + diagonal2Score
	
	def scorePosition(self, board, row, column, deltaROW, deltaCOL):
		'''
			Hueristic evaluation for current state
			+1000, +100, +10, +1 for 4-,3-,2-,1-in-a-line for AI player
			-1000, -100, -10, -1 for 4-,3-,2-,1-in-a-line for human player
			0 otherwise
		'''
		humanScore = 0
		AIScore = 0
		humanPoints = 0
		AIPoints = 0
		for i in range(4):
			currentChip = board.getChip(row, column)
			if currentChip == self.chip: #if current chip is AI
				AIPoints += 1
			elif currentChip == 'O': #player chip
				humanPoints += 1
			row += deltaROW
			column += deltaCOL

		if humanPoints == 1: 
			humanScore = pow(-10, 0) # -1 point
		elif humanPoints == 2:
			humanScore = pow(-10, 1) # -10 points
		elif humanPoints == 3:
			humanScore = pow(-10, 2) # -100 points
		elif humanPoints == 4:
			humanScore = pow(-10, 3) # -1000 points
		# 0 otherwise

		if AIPoints == 1: 
			AIScore = pow(10, 0) # 1 point
		elif AIPoints == 2:
			AIScore = pow(10, 1) # 10 points
		elif AIPoints == 3:
			AIScore = pow(10, 2) # 100 points
		elif AIPoints == 4:
			AIScore = pow(10, 3) # 1000 points
		# 0 otherwise

		return humanScore + AIScore

	def miniMax(self, player, board, depth, alpha = -INFINITY, beta = INFINITY):
		#time.sleep(0.1)
		nextMoves = self.generateMoves(board)
		score = None
		bestRow = -1
		bestColumn = -1
		if not nextMoves or depth == 0: #if list of next moves is empty or or reached root
			score = self.evaluateHeuristic(board)
			if self.showScores: print("Score: {:6} | Alpha: {:6} | Beta: {:6}".format(score, alpha, beta))
			return score, bestRow, bestColumn
		else:
			for move in nextMoves:
				#try move
				board.addChip(player, move[0], move[1])
				if player == self.chip: #if player is AI (max), switch to human (min)
					#MIN
					score = self.miniMax('O', board, depth-1, alpha, beta)[0]
					if score > alpha:
						alpha = score
						bestRow = move[0]
						bestColumn = move[1]
				else: #player is human (min), then switch to AI (max)
					#MAX
					score = self.miniMax(self.chip, board, depth-1, alpha, beta)[0]
					if score < beta:
						beta = score
						bestRow = move[0]
						bestColumn = move[1]
				if self.showScores: print("Score: {:6} | Alpha: {:6} | Beta: {:6}".format(score, alpha, beta))
				#undo move
				board.removeChip(move[0], move[1])
				if alpha >= beta:
					if self.showScores: print("PRUNING!")
					break
		return alpha if player == self.chip else beta, bestRow, bestColumn

