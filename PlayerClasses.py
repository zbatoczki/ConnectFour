from abc import ABC, ABCMeta, abstractmethod

class Player(metaclass=ABCMeta):
	"""docstring for Player"""
	chip = "" #'O' or 'X'

	def __init__(self, chip):
		self.chip = chip

	@abstractmethod
	def playTurn(self):
		pass

class Human(Player):
	def __init__(self, chip):
		super(Human, self).__init__(chip)

	def playTurn(self, board):
		#chipPosition = ()
		column = int(input("Pick a column > "))
		column -= 1
		while True:
			row = board.canAddChip(column) #tuple (can add chip[bool], row)
			if board.isValidColumn(column) and row[0]:
				#attempt to add chip, ask input if failed
				board.addChip(self.chip, row[1], column)
				break
			column = int(input("That column did not work. Try a different column > "))
			column -= 1
		return row[1], column	