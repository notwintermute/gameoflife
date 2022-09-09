import math
import pygame
import numpy as np
import time

sqSide = 20 # side length of a square
noSX = 50 # number of squares width-wise
noSY = 30 # number of squares height-wise
resX = sqSide * noSX
resY = sqSide * noSY
n = noSY
m = noSX
fps = 10
#############
# making the mult column matrix
line2 = np.zeros((1, n))
line2[0, 0:2] = 1
aMul = line2
line3 = np.zeros((1, n + 1))
line3[0, 0:3] = 1
for i in range(n - 3):
    aMul = np.concatenate((aMul, line3), axis=1)
aMul = np.concatenate((aMul, np.ones((1, 3))), axis=1)
aMul = np.concatenate((aMul, np.zeros((1, n))), axis=1)
aMul[0, -1] = aMul[0, -2] = 1
aMul = aMul.reshape((n, n))

Mul1 = aMul


# making the mult row matrix
line2 = np.zeros((1, m))
line2[0, 0:2] = 1
aMul = line2
line3 = np.zeros((1, m + 1))
line3[0, 0:3] = 1
for i in range(m - 3):
    aMul = np.concatenate((aMul, line3), axis=1)
aMul = np.concatenate((aMul, np.ones((1, 3))), axis=1)
aMul = np.concatenate((aMul, np.zeros((1, m))), axis=1)
aMul[0, -1] = aMul[0, -2] = 1
aMul = aMul.reshape((m, m))

Mul2 = aMul

################
playing = 0
time1 = time.time()
grid = np.zeros((n, m))  # grid where amount is stored

print(grid)
emitters = []
brushSize = 0
drawing = False
erasing = False
pygame.init()

# initialize surface and start the main loop
surface = pygame.display.set_mode((resX, resY))
pygame.display.set_caption('Game of Life')
running = True
# --------------------------------------- Main Loop ---------------------------------------
while running:
    mouse = pygame.mouse.get_pos()  # puts the mouse position into a 2d tuple
    mouseSq = [math.floor(mouse[0] / sqSide), math.floor(mouse[1] / sqSide)]
    # ------------------------------------- input handling -------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # ------------------------------------ mouse click actions ------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
            if event.button == 3:
                erasing = True
        if event.type == pygame.MOUSEBUTTONUP:  # releasing the hold
            drawing = False
            erasing = False
        # ------------------------------------ key press actions ------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("Row : ", mouseSq[1])
                print("Column : ", mouseSq[0])
            if event.key == pygame.K_s:
                playing += 1
                playing %= 2
            if event.key == pygame.K_e:
                sum1 = np.matmul(Mul1, grid)
                sum = np.matmul(Mul2, sum1.transpose()).transpose() - grid
                s2 = (1 * (sum == 2))
                s3 = (1 * (sum == 3))
                live = 1 * ((grid + s2) == 2)
                grid = (s3 + live)
                time1 = time.time()

    # ---------------------------------------- Updating Parameters ----------------------------------------
    if drawing:
        grid[mouseSq[1], mouseSq[0]] = 1
    if erasing:
        grid[mouseSq[1], mouseSq[0]] = 0

    if time.time()-time1 > (1/fps) and playing:
        sum1 = np.matmul(Mul1, grid)
        sum = np.matmul(Mul2, sum1.transpose()).transpose() - grid
        s2 = (1 * (sum == 2))
        s3 = (1 * (sum == 3))
        live = 1 * ((grid + s2) == 2)
        grid = (s3 + live)
        time1 = time.time()
    # ---------------------------------------- Rendering ----------------------------------------
    for y in range(n):
        for x in range(m):
            color = (255*grid[y, x], 255*grid[y, x], 255*grid[y, x])
            pygame.draw.rect(surface, color, (x * sqSide, y * sqSide, sqSide, sqSide))
            pygame.draw.rect(surface, (155, 155, 155), (x * sqSide, y * sqSide, sqSide, sqSide), width=1)


    pygame.display.flip()
