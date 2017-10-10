import math, time
from PlayerClasses import Player

INFINITY = math.inf
class AI(Player):	
	depth = None
	def __init__(self, chip='X'):
		super(AI, self).__init__(chip)
		self.setDifficulty()

	def setDifficulty(self):
		self.depth = int(input("Enter a difficulty from 1 to 6.\nYou can go higher, but performance will take longer.\n> "))

	def playTurn(self, board):
		#print("Enemy turn...")
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

		'''	// Vertical points
		    // Check each column for vertical score
		    // 
		    // Possible situations
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
				#print("VERTICAL SCORE: ", verticalScore)

		'''
			// Horizontal points
		    // Check each row's score
		    // 
		    // Possible situations
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
				#print("HORIZONTAL SCORE: ", horizontalScore)

		'''	// Diagonal points 1 (negative-slope)
		    //
		    // Possible situation
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
				#print("DIAGONAL 1 SCORE: ", diagonal1Score)

		'''
		    // Diagonal points 2 (right-bottom)
		    //
		    // Possible situation
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
				#print("DIAGONAL 2 SCORE: ", diagonal2Score)

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
		nextMoves = self.generateMoves(board)
		#print("---POSSIBLE MOVES---\n", nextMoves, end="\n\n")
		score = None
		bestRow = -1
		bestColumn = -1
		if not nextMoves or depth == 0: #if list of next moves is empty or or reached root
			score = self.evaluateHeuristic(board)
			#print("SCORE FROM MINIMAX: ", score)
			#print("================================================\n")
			return score, bestRow, bestColumn
		else:
			for move in nextMoves:
				#try move
				board.addChip(player, move[0], move[1])
				if player == self.chip: #if player is AI (max), switch to human (min)
					#print("CALLING MIN...")
					score = self.miniMax('O', board, depth-1, alpha, beta)[0]
					if score > alpha:
						alpha = score
						bestRow = move[0]
						bestColumn = move[1]
				else: #player is human (min), then switch to AI (max)
					#print("CALLING MAX...")
					score = self.miniMax(self.chip, board, depth-1, alpha, beta)[0]
					if score < beta:
						beta = score
						bestRow = move[0]
						bestColumn = move[1]

				#undo move
				board.removeChip(move[0], move[1])
				if alpha >= beta:
					break
		return alpha if player == self.chip else beta, bestRow, bestColumn

