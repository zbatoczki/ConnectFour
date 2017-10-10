class GameBoard:
	board = []
	boardWidth = 7
	boardHeight = 6

	def __init__(self):
		self.setBoard()
		
	def setBoard(self):
		for row in range(self.boardHeight):
			self.board.append([])
			for column in range(self.boardWidth):
				self.board[row].append('-')

	def resetBoard(self):
		for row in range(self.boardHeight):
			for column in range(self.boardWidth):
				self.board[row][column] = '-'

	def printBoard(self):
		for i in range(self.boardHeight):
			print("| ", end="")
			print(*self.board[i], sep=" | ", end="")
			print(" |\n")

	def isValidColumn(self, column):
		return False if column < 0 or column >= self.boardWidth else True

	def getChip(self, row, column):
		return self.board[row][column]

	'''Check if there is room to add in a chip
		return row if chip can be added'''
	def canAddChip(self, column):
		for i in range( (self.boardHeight-1), -1, -1): #from 5 to 0
			if self.board[i][column] == '-':
				return True, i
		return False, -1

	def addChip(self, chip, row, column):
		'''check if there is room for a chip to add
			starting from bottom, return true if spot empty, 	false otherwise
		'''
		self.board[row][column] = chip

	def removeChip(self, row, column):
		self.board[row][column] = '-'

	def isWinner(self, chip):
		
		ticks = 0
		# vertical
		for row in range(self.boardHeight - 3):
			for column in range(self.boardWidth):
				ticks = self.checkAdjacent(chip, row, column, 1, 0)
				if ticks == 4: return True
		# horizontal
		for row in range(self.boardHeight):
			for column in range(self.boardWidth - 3):
				ticks = self.checkAdjacent(chip, row, column, 0, 1)
				if ticks == 4: return True
		# positive slope diagonal
		for row in range(self.boardHeight-3):
			for column in range(self.boardWidth - 3):
				ticks = self.checkAdjacent(chip, row, column, 1, 1)
				if ticks == 4: return True
		#negative slope diagonal
		for row in range(3, self.boardHeight):
			for column in range(self.boardWidth - 5):
				ticks = self.checkAdjacent(chip, row, column, -1, 1)
				if ticks == 4: return True
		return False

	def checkAdjacent(self, chip, row, column, deltaROW, deltaCOL):
		count = 0
		for i in range(4):
			currentChip = self.getChip(row, column)
			if currentChip == chip:
				count += 1
			row += deltaROW
			column += deltaCOL
		return count

'''CHECK WINNER - FIRST VERSION
	def isWinner(self, chip, position):

		row = position[0]
		col = position[1]		
		ticks = 1	
		#check up (I don't believe this is necessary)

		#check down
		#ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row+1, col, 'down', ticks)
		if ticks == 4: return True

		#check left
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row, col-1, 'left', ticks)
		if ticks == 4: return True

		#check right
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row+1, col, 'right', ticks)
		if ticks == 4: return True

		#check upright diagonal
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row-1, col+1, 'upright', ticks)
		if ticks == 4: return True

		#check downleft diagonal
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row+1, col-1, 'downleft', ticks)
		if ticks == 4: return True

		#check upleft diagonal
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row-1, col-1, 'upleft', ticks)
		if ticks == 4: return True
		
		#check downright diagonal
		ticks = 1 #reset ticks
		ticks = self.checkNeighbor(chip, row+1, col+1, 'downright', ticks)
		if ticks == 4: return True

		return False

	def checkNeighbor(self, chip, row, column, direction, ticks):		
		if ticks >= 4 or row < 0 or row >= self.boardHeight or column < 0 or column >= self.boardWidth or self.board[row][column] != chip:
			return ticks
		#up
		elif direction == "up": row -= 1
		#down
		elif direction == "down": row += 1
		#left
		elif direction == "left": column -= 1
		#right
		elif direction == "right": column += 1
		#upright
		elif direction == "upright": 
			row -= 1
			column += 1
		#upleft
		elif direction == "upleft": 
			row -= 1
			column -= 1
		#downright
		elif direction == "downright": 
			row += 1
			column += 1
		#downleft
		elif direction == "downleft": 
			row += 1
			column -= 1
		ticks += 1		
		return self.checkNeighbor(chip, row, column, direction, ticks)
'''