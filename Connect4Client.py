# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 18:18:39 2017

@author: ZES
"""
from PlayerClasses import Player, Human 
from AIClass import AI
from GameBoard import GameBoard
class GameClient:
	board = None
	human = None
	ai = None
	winnerFound = False
	humansTurn = True
	currentRound = 1
	MAX_ROUNDS = 42 #max number of turns before game baord is full

	def __init__(self):
		self.board = GameBoard()
		self.human = Human('O')
		self.ai = AI('X')		

	def play(self):
		print("Playing game...")
		self.board.printBoard()
		winner = "It's a DRAW!"
		while self.currentRound <= self.MAX_ROUNDS and not self.winnerFound:
			if self.humansTurn:
				print("Player's turn...")
				playedChip = self.human.playTurn(self.board)
				self.winnerFound = self.board.isWinner(self.human.chip)
				if self.winnerFound: winner = "PLAYER wins!"
				self.humansTurn = False
			else:
				print("AI's turn...")
				playedChip = self.ai.playTurn(self.board)
				self.winnerFound = self.board.isWinner(self.ai.chip)
				if self.winnerFound: winner = "AI wins!"
				self.humansTurn = True
			self.currentRound += 1
			self.board.printBoard()
		return winner

	def reset(self):
		#reset variables
		self.currentRound = 1
		self.winnerFound = False
		self.humansTurn = True
		self.board.resetBoard()
		self.ai.setDifficulty()

def endGame(winner):
	print(winner, end=" ")
	userInput = input("Play again? (Y/N)\n").lower()
	return True if userInput == 'y' else False 

if __name__ == "__main__":
	gameClient = GameClient()
	winner = gameClient.play()
	playAgain = endGame(winner)
	while playAgain:
		gameClient.reset()
		winner = gameClient.play()
		playAgain = endGame(winner) 