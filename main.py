import pygame
from Classes import Square, Agent
import random
from const import boardlen
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib

matplotlib.use("TkAgg")

generations_data = []
steps_data = []

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots(figsize=(8, 5))
(line,) = ax.plot([], [], "bo-", label="Steps to Goal")
(trend_line,) = ax.plot([], [], "r--", alpha=0.7, label="Trend")
ax.set_title("Steps to Reach Goal vs Generation")
ax.set_xlabel("Generation")
ax.set_ylabel("Steps")
ax.grid(True)
ax.legend()
plt.tight_layout()


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True

steps = 0

squares = []
for i in range(boardlen):
    squares.append([])
    for j in range(boardlen):
        squares[i].append(
            Square(screen, i * 1000 / boardlen, j * 1000 / boardlen, i, j)
        )


def update_plot():
    if len(generations_data) > 0:
        # Update data
        line.set_data(generations_data, steps_data)

        # Update axes limits
        ax.set_xlim(0, max(generations_data) + 1)
        ax.set_ylim(0, max(steps_data) * 1.1)

        # Update trend line if we have enough data
        if len(generations_data) > 1:
            try:
                z = np.polyfit(generations_data, steps_data, 1)
                p = np.poly1d(z)
                x_range = np.array([min(generations_data), max(generations_data)])
                trend_line.set_data(x_range, p(x_range))
            except:
                pass  # Skip trend line if fitting fails

        # Redraw the plot
        fig.canvas.draw_idle()
        fig.canvas.flush_events()


squares[random.randrange(0, boardlen)][random.randrange(0, boardlen)].setWin()
agent = Agent(
    squares[random.randrange(0, boardlen)][random.randrange(0, boardlen)], squares
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    agent.step()
    steps += 1
    # print(len(agent.visitedSquares))
    # print(agent.moves)
    for row in squares:
        for s in row:
            s.drawRect()
            if running:
                running = s.checkWin()
                if not running:
                    agent.notifyWin()
                    running = True
                    print(
                        "Reached goal in : "
                        + str(steps)
                        + " Steps in Generation : "
                        + str(agent.generation)
                    )
                    generations_data.append(agent.generation)
                    steps_data.append(steps)

                    update_plot()

                    steps = 0
                    continue

                running = s.checkLose()
                if not running:
                    # agent.notifyLose()
                    running = True
                    continue

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(50)


plt.ioff()
plt.savefig("learning_progress_final.png")
plt.close()

pygame.quit()
