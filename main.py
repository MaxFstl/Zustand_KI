import pygame 
from Classes import Square, Agent
import random
from const import boardlen

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

steps = 0

squares = []
for i in range(boardlen):
    squares.append([])
    for j in range(boardlen):
        squares[i].append(Square(screen, i*1000/boardlen, j*1000/boardlen, i, j))

#squares[1][1].setWin()
#squares[6][6].setLose()
#squares[2][2].setWin()
#squares[3][3].setWin()
#squares[4][4].setWin()
squares[random.randrange(0,boardlen)][random.randrange(0,boardlen)].setWin()
agent = Agent(squares[random.randrange(0,boardlen)][random.randrange(0,boardlen)], squares)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("skyblue")

    agent.step()
    steps += 1
    #print(len(agent.visitedSquares))
   # print(agent.moves)
    for row in squares:
        for s in row:
            s.drawRect()
            if running:
                running = s.checkWin()
                if not running:
                    agent.notifyWin()
                    running = True
                    print("Reached goal in : " + str(steps)+ " Steps in Generation : " + str(agent.generation))
                    steps = 0
                    continue

                running = s.checkLose()
                if not running:
                    #agent.notifyLose()
                    running = True
                    continue
                
            
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(20000)

pygame.quit()