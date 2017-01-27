import random
# pip name for package is pillow
from PIL import Image

PURPLE = (185, 100, 200)
GREEN = (200, 220, 170)
UNVISITED = 0;
PATH = 1

imageSizeX = 410;
imageSizeY = 410
mazeResX = 41;
mazeResY = 41

startCell = int(mazeResX/2) * (int(mazeResY/2))
stack = [startCell]

maze = [UNVISITED for i in range(mazeResX * mazeResY)]
maze[startCell] = PATH

def GetNeighbourIDs(cellID):
    neighbours = []
    if cellID > mazeResX * 2: #not on top row
        neighbours.append(cellID - mazeResX * 2)
    if cellID % mazeResX < mazeResX - 2: #not on right col
        neighbours.append(cellID + 2)
    if cellID < (mazeResY - 2) * mazeResX: #not on bottom row
        neighbours.append(cellID + mazeResX * 2)
    if cellID % mazeResX > 2: #not on left col
        neighbours.append(cellID - 2)
    return neighbours

def GetUnvisitedNeighbourIDs(cellID):
    neighbours = GetNeighbourIDs(cellID)
    unvisited = []
    for neighbourID in neighbours:
        if maze[neighbourID] == UNVISITED:
            unvisited.append(neighbourID)
        elif neighbourID == stack[-2]:
            maze[int((neighbourID + cellID)/2)] = PATH
    return unvisited

def ChooseDirection(numUnvisit):
    # if prev direction is still available, 2/3 chance of staying
    
    compass = random.randint(0, numUnvisit - 1)
    return compass

def VisitCell(cellID):
    neighbours = GetUnvisitedNeighbourIDs(cellID)
    numUnvisit = len(neighbours)
    if numUnvisit == 0:
        stack.pop()
    else:
        direction = ChooseDirection(numUnvisit)
        for i in range(numUnvisit):
            neighbourID = neighbours[(i + direction) % numUnvisit]
            maze[neighbourID] = PATH
            stack.append(neighbourID)
            VisitCell(stack[-1])
    if len(stack) > 2:
        VisitCell(stack[-1])

def DrawImage():
    VisitCell(startCell)    
    image = Image.new("RGB", (imageSizeX, imageSizeY))
    pixels = image.load()
    xRes = int(imageSizeX/mazeResX)
    yRes = int(imageSizeY/mazeResY)
    for i in range(mazeResY):
        for j in range(mazeResX):
            for y in range(yRes):                
                for x in range(xRes):
                    colour = GREEN if (maze[i * mazeResX + j] == PATH) else PURPLE
                    pixels[x + j * xRes, y + i * yRes] = colour
    image.save("JennyMaze_" + str(mazeResX) + "x" + str(mazeResY) + ".png", "PNG")

DrawImage()
