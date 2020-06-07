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
size_of_diagram = 10
points_from_file = [0, 0, 0]
points_default = [[0, 0, 0], [size_of_diagram - 1, size_of_diagram - 1, size_of_diagram - 1], [size_of_diagram - 1, 0, 0]]


def Voronoi3D(points):
    result_table = np.zeros([size_of_diagram, size_of_diagram, size_of_diagram], np.int)

    for table_index, table in enumerate(result_table):
        for row_index, row in enumerate(table):
            for column_index, column in enumerate(row):
                current_distance = size_of_diagram * size_of_diagram * size_of_diagram
                current_point = "X"
                for index_of_voxel, current_voxel in enumerate(points):
                    distance_from_current_voxel_to_point = distance3d(table_index, row_index, column_index, current_voxel[0], current_voxel[1], current_voxel[2])
                    if current_distance > distance_from_current_voxel_to_point:
                        current_distance = distance_from_current_voxel_to_point
                        current_point = index_of_voxel+1
                result_table[table_index][row_index][column_index] = current_point
    return result_table


def is_valid_index_of_point(string_with_indexes_of_point):
    for index in string_with_indexes_of_point:
        if not index.isdigit():
            return False
    return True


def distance3d(x1, y1, z1, x2, y2, z2):
    distance = sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return distance


def load_file():
    global points_from_file
    local_list_of_points = np.empty((0,3), int)
    filename = fd.askopenfilename(initialdir=".", title="Select file", filetype=(("Text file", "*.txt"), ("All files", "*.*")))
    if filename:
        with open(filename,"r") as f:
            content_of_file_of_points = "".join(f.read().split())
            string_from_list_of_points = content_of_file_of_points.split(";")
            for point in string_from_list_of_points:
                index_of_point = point.split(",")
                if is_valid_index_of_point(index_of_point):
                    local_list_of_points = np.append(local_list_of_points, np.array([list(map(int, index_of_point))]), axis=0)
                else:
                    continue
        points_from_file = local_list_of_points


def recalculate_for_new_set_of_points():
    draw_voronoi3d_diagram(points_from_file)


def table_for_points(points):
    table_of_points = np.zeros([size_of_diagram, size_of_diagram, size_of_diagram], np.int)
    for point in points:
        table_of_points[[point[0]], [point[1]], [point[2]]] = True
    return table_of_points


def table_of_areas_for_points(list_of_points, voronoi_table):
    list_of_points = list(range(1, np.shape(list_of_points)[0] + 1))
    list_of_area_matrix = []
    for indexOfPoint in list_of_points:
        area_matrix_for_one_color = np.zeros(voronoi_table.shape, np.int)
        area_matrix_for_one_color[np.nonzero(voronoi_table == indexOfPoint)] = 1
        list_of_area_matrix.append([indexOfPoint, area_matrix_for_one_color])
    return list_of_area_matrix


def draw_voronoi3d_diagram(points):
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    for area in table_of_areas_for_points(points, Voronoi3D(points)):
        random_color_hex = '#' + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + "30"
        #print(random_color_hex)
        ax.voxels(area[1], facecolors=random_color_hex, edgecolors=None, shade=False)
    ax.voxels(table_for_points(points), facecolor='black', edgecolors='black', shade=False)

    canvas.get_tk_widget().place(x=150, y=5)
    return canvas


#Ogolne
root = tk.Tk()
root.geometry("660x500")
root.wm_title("Voronoi3D")
root.resizable(False, False)

#Definiowanie elementow GUI
load_button = tk.Button(root, text="Wczytaj punkty z pliku", command=load_file, height=1, width=18)
recalculate_button = tk.Button(root, text="Przelicz", command=recalculate_for_new_set_of_points, height=1, width=18)

#Rysowanie wykresu 3D Voronoi
canvas = draw_voronoi3d_diagram(points_default)
toolbar = NavigationToolbar2Tk(canvas, root)

#Pozycjonowanie elementow GUI
load_button.place(x=5, y=5)
recalculate_button.place(x=5, y=35)
toolbar.update()
root.mainloop()