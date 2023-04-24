import pygame as pg
import random
from const import boardlen

class Square:

    width = 1000/boardlen
    x = 0
    y = 0
    surface = None
    color = "#000000"
    


    player = False
    win = False
    lose = False

    xPosOnBoard = 0
    yPosOnBoard = 0


    policy = "N"
    value : int = 0



    def drawRect(self):
        
        #text = self.font.render(str(int(self.value)), True, (0, 0, 0))
        #text = self.font.render(self.policy + " , " +str(self.value), True, (0,0,0))
       # self.surface.blit(text, (self.x +4, self.y+4))

        if self.player:
            pg.draw.rect(self.surface, "yellow", pg.Rect(
                self.x, self.y, self.width, self.width),  int(self.width/2))
            return
        
        if self.win:
            pg.draw.rect(self.surface, "green", pg.Rect(
                self.x, self.y, self.width, self.width),  int(self.width/2))
            return
        
        if self.lose:
            pg.draw.rect(self.surface, "red", pg.Rect(
                self.x, self.y, self.width, self.width),  1)
            return

        pg.draw.rect(self.surface, self.color, pg.Rect(
            self.x, self.y, self.width, self.width),  1)
        

    def __init__(self, surface: pg.Surface, x: float, y: float, xPosOnBoard : int, yPosOnBoard : int):
        pg.font.init()
        self.font = pg.font.SysFont('arial', 30)
        self.surface = surface
        self.x = x
        self.y = y
        self.xPosOnBoard = xPosOnBoard
        self.yPosOnBoard = yPosOnBoard

    def checkWin(self):
        if self.player and self.win:
            return False
        return True
    
    def checkLose(self):
        if self.player and self.lose:
            return False
        return True  
    
    def setWin(self):
        self.win = True
        self.value = 100

    def setLose(self):
        self.lose = True
        self.value = -100

class Agent:
    exploration = 0.7
    discount = 1 - 1/boardlen
    generation = 1
    currSquare : Square
    board = []
    visitedSquares : Square = []
    moves = []

    def __init__(self, currSquare : Square, board):
        #self.currSquare = currSquare
        self.board = board
        #self.currSquare.player = True
        self.placeAgent(currSquare.xPosOnBoard, currSquare.yPosOnBoard)

    def step(self):
        e = random.random()

        #Random move
        if e > self.exploration  and self.generation < pow(boardlen , 4) or self.currSquare.policy == "N":
            m = random.randint(0,3)
            if m == 0:
                    self.moves.append("R")
                    self.movePlayer(1,0)
            if m == 1:
                    self.moves.append("L")
                    self.movePlayer(-1,0)
            if m == 2:
                    self.moves.append("D")
                    self.movePlayer(0,1)
            if m == 3:
                    self.moves.append("U")
                    self.movePlayer(0,-1)

        else:
            if self.currSquare.policy == "U":
                self.moves.append("U")
                self.movePlayer(0,-1)
            if self.currSquare.policy == "L":
                self.moves.append("L")
                self.movePlayer(-1,0)
            if self.currSquare.policy == "R":
                self.moves.append("R")
                self.movePlayer(1,0)
            if self.currSquare.policy == "D":
                self.moves.append("D")
                self.movePlayer(0,1)

    def movePlayer(self, xDir:int, yDir:int):
        #Spieler bewegt sich in x Richtung
        if yDir == 0:
            if self.currSquare.xPosOnBoard == boardlen-1 and xDir == 1:
                #self.visitedSquares.append(self.currSquare)
                self.moves.pop()
                return
            if self.currSquare.xPosOnBoard == 0 and xDir == -1:
                #self.visitedSquares.append(self.currSquare)
                self.moves.pop()
                return
            self.currSquare.player = False
            s = self.currSquare
            self.currSquare = self.board[self.currSquare.xPosOnBoard+xDir][self.currSquare.yPosOnBoard]
            self.visitedSquares.append(self.currSquare)
            self.currSquare.player = True

        #Spieler bewegt sich in y Richtung
        if xDir == 0:
            if self.currSquare.yPosOnBoard == boardlen -1 and yDir == 1:
                #self.visitedSquares.append(self.currSquare)
                self.moves.pop()                
                return
            if self.currSquare.yPosOnBoard == 0 and yDir == -1:
                #self.visitedSquares.append(self.currSquare)
                self.moves.pop()                
                return
            self.currSquare.player = False
            s = self.currSquare
            self.currSquare = self.board[self.currSquare.xPosOnBoard][self.currSquare.yPosOnBoard + yDir]
            self.visitedSquares.append(self.currSquare)

            self.currSquare.player = True

    def notifyWin(self):
        self.visitedSquares.reverse()
        self.moves.reverse()
        for i in range(1,len(self.visitedSquares)):
            prev_val = self.visitedSquares[i-1].value
            if prev_val * self.discount > self.visitedSquares[i].value:
                self.visitedSquares[i].value = prev_val* self.discount
                self.visitedSquares[i].policy = self.moves[i-1]
        self.moves.clear()
        self.visitedSquares.clear()
        self.currSquare.player = False
        self.placeAgent(random.randint(0,boardlen-1), random.randint(0,boardlen-1))
        self.generation += 1
   # def notifyLose(self):

        #s = self.visitedSquares[len(self.visitedSquares) -1]
        #move = self.moves[len(self.moves) - 1]
       # if move == "L":


            
        #self.visitedSquares[len(self.visitedSquares) -1].player = False
        #self.placeAgent(random.randint(0,9), random.randint(0,9))
        #self.moves.clear()
        #self.visitedSquares.clear()


    def placeAgent(self, posx, posy):
        self.board[posx][posy].player = True
        self.currSquare = self.board[posx][posy]
        self.visitedSquares.append(self.currSquare)