import tkinter as tk
from tkinter import filedialog as fd
from math import sqrt
import numpy as np
from matplotlib.figure import Figure
import random
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#Ew. zamiast liczyc odleglosci miedzy voxelami a punktami mozna wyliczyc dla pktow scipy.spatial.Delaunay ( triangulacje Delaunaya )
#Dla N wymiarowej przestrzeni zrzuca N wymiarowa triangulacje czyli dziala dla 3D
#Wynik to będzie lista punktow ktore mozna polaczyc korzystajac z scipy.spatial.ConvexHull
#Np. https://stackoverflow.com/questions/27270477/3d-convex-hull-from-point-cloud
#Wtedy rysowanie GUI byłoby płynniejsze bo nie musiałby renderować obiektow 3D tylko linie.

#3D:
#Początkowy zestaw punktow do Voronoi3D:
sizeOfDiagram = 10
pointsFromFile = [0, 0, 0]
pointsDefault = [[0, 0, 0], [sizeOfDiagram - 1, sizeOfDiagram - 1, sizeOfDiagram - 1], [sizeOfDiagram - 1, 0, 0]]

def Voronoi3D(points):
    global sizeOfDiagram
    resultTable = np.zeros([sizeOfDiagram, sizeOfDiagram, sizeOfDiagram], np.int)

    for tableIndex, table in enumerate(resultTable):
        for rowIndex, row in enumerate(table):
            for columnIndex, column in enumerate(row):
                currentDistance = sizeOfDiagram * sizeOfDiagram * sizeOfDiagram
                currentPoint = "X"
                for voxelIndex, currentVoxel in enumerate(points):
                    distanceFromCurrentVoxelToPoint = distance3d(tableIndex, rowIndex, columnIndex, currentVoxel[0], currentVoxel[1], currentVoxel[2])
                    if currentDistance > distanceFromCurrentVoxelToPoint:
                        currentDistance = distanceFromCurrentVoxelToPoint
                        currentPoint = voxelIndex+1
                resultTable[tableIndex][rowIndex][columnIndex] = currentPoint
    return resultTable

def isValidIndexOfPoint(stringWithIndexesOfPoint):
    for index in stringWithIndexesOfPoint:
        if not index.isdigit():
            return False
    return True

def distance3d(x1, y1, z1, x2, y2, z2):
    distance = sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return distance

def LoadFile():
    global pointsFromFile
    localListOfPoints = np.empty((0,3), int)
    filename = fd.askopenfilename(initialdir=".", title="Select file",filetype=(("Text file","*.txt"),("All files","*.*")) )
    if filename:
        with open(filename,"r") as f:
            contentOfFileOfPoints = "".join(f.read().split())
            stringFromListOfPoints = contentOfFileOfPoints.split(";")
            for point in stringFromListOfPoints:
                indexOfPoint = point.split(",")
                if (isValidIndexOfPoint(indexOfPoint)):
                    localListOfPoints = np.append(localListOfPoints,np.array([list(map(int, indexOfPoint))]),axis=0)
                else:
                    continue
        pointsFromFile = localListOfPoints

def RecalculateForNewSetOfPoints():
    global pointsFromFile
    DrawVoronoi3DDiagram(pointsFromFile)

def TableForPoints(points):
    global sizeOfDiagram
    tableOfPoints = np.zeros([sizeOfDiagram, sizeOfDiagram, sizeOfDiagram], np.int)
    for point in points:
        tableOfPoints[[point[0]],[point[1]],[point[2]]]=True
    return tableOfPoints

def TableOfAreasForPoints(punkty, VoronoiTable):
    listOfPoints = list(range(1, np.shape(punkty)[0]+1))
    listOfAreaMatrix = []
    for indexOfPoint in listOfPoints:
        AreaMatrixForOneColor = np.zeros(VoronoiTable.shape, np.int)
        AreaMatrixForOneColor[np.nonzero(VoronoiTable == indexOfPoint)] = 1
        listOfAreaMatrix.append([indexOfPoint, AreaMatrixForOneColor])
    return listOfAreaMatrix

def DrawVoronoi3DDiagram(points):
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    ax = fig.add_subplot(1, 1, 1, projection="3d")
    for obszar in TableOfAreasForPoints(points, Voronoi3D(points)):
        randomColorHex = '#' + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') +"30"
        print(randomColorHex)
        ax.voxels(obszar[1], facecolors=randomColorHex, edgecolors=None, shade=False)
    ax.voxels(TableForPoints(points), facecolor='black', edgecolors='black', shade=False)

    canvas.get_tk_widget().place(x=150, y=5)
    return canvas

#Ogolne
root = tk.Tk()
root.geometry("660x500")
root.wm_title("Voronoi3D")
root.resizable(False, False)

#Definiowanie elementow GUI
LoadButton = tk.Button(root, text="Wczytaj punkty z pliku", command=LoadFile, height=1, width=18)
RecalculateButton = tk.Button(root, text="Przelicz", command=RecalculateForNewSetOfPoints, height=1, width=18)

#Rysowanie wykresu 3D Voronoi
canvas = DrawVoronoi3DDiagram(pointsDefault)
toolbar = NavigationToolbar2Tk(canvas, root)

#Pozycjonowanie elementow GUI
LoadButton.place(x = 5, y = 5)
RecalculateButton.place(x = 5, y = 35)
toolbar.update()
root.mainloop()