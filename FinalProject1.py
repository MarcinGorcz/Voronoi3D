import tkinter as tk
from tkinter import filedialog as fd
from math import sqrt
import numpy as np
from matplotlib.figure import Figure
import random
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#Początkowy zestaw punktow do Voronoi3D:
size_of_diagram = 10
#tablica na punkty z pliku:
points_from_file = [0, 0, 0]
#tablica na startowy zestaw punktow
points_default = [[0, 0, 0], [size_of_diagram - 1, size_of_diagram - 1, size_of_diagram - 1], [size_of_diagram - 1, 0, 0]]


def Voronoi3D(points):
    #pusta tablica pomocnicza zawieracja diagram gdzie to czy voxel jest w danym obszarze jest oznaczane numerem punktu.
    result_table = np.zeros([size_of_diagram, size_of_diagram, size_of_diagram], np.int)

    #przechodzenie voxel po voxelu z tablicy pomocniczej
    for table_index, table in enumerate(result_table):
        for row_index, row in enumerate(table):
            for column_index, column in enumerate(row):
                #inicjalizuje pomocniczy current distance wiekszy niz jakikolwiek dystans ktory otrzymam dla tablicy
                current_distance = size_of_diagram * size_of_diagram * size_of_diagram
                current_point = "X"
                #dla kazdego voxelu z tabllicy pomocniczej sprawdzam odleglosc do kazdego z punktow dla danego zestawu
                #punktow i przypisuje mu (voxelowi) indeks w liscie tego punktu do ktorego ma najmniejszy dystans.
                #jesli dystans bedzie taki sam to uznalem ze jest to obojene ktory pokaze więc dostanie go ostatni punkt
                for index_of_voxel, current_voxel in enumerate(points):
                    distance_from_current_voxel_to_point = distance3d(table_index, row_index, column_index, current_voxel[0], current_voxel[1], current_voxel[2])
                    if current_distance > distance_from_current_voxel_to_point:
                        current_distance = distance_from_current_voxel_to_point
                        current_point = index_of_voxel+1
                result_table[table_index][row_index][column_index] = current_point
    return result_table

#sprawdzanie przy wczytywaniu punktow z pliku, czy kazdy wczytany index punktu(x,y,z) jest liczba.
#jesli nie jest punkt jest pominiety
def is_valid_index_of_point(string_with_indexes_of_point):
    for index in string_with_indexes_of_point:
        if not index.isdigit():
            return False
    return True

#liczenie dystansu miedzy punktami w przestrzeni 3D czyli pierwiastek kwadratowy z sumy kwadratow roznic ich wspolrzednych
def distance3d(x1, y1, z1, x2, y2, z2):
    distance = sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return distance

#Funkcja wczytywania z pliku podpieta do przycisku
#Wczytuje punkty z pliku i zapisuje je w zmiennej points_of_file
def load_file():
    global points_from_file
    local_list_of_points = np.empty((0,3), int)
    #Otworzenie okna wybierania pliku, dla plikow tekstowych txt ew wszystkich )
    filename = fd.askopenfilename(initialdir=".", title="Select file", filetype=(("Text file", "*.txt"), ("All files", "*.*")))
    if filename:
        with open(filename,"r") as f:
            #Otwieram zawartosc pliku jako string, kolejne punkty oddzielone sa ; a kolejne wspolrzedne ,
            #Wczytuje caly plik usuwajac znaki biale
            content_of_file_of_points = "".join(f.read().split())
            #Tworze liste puntow jako strigow w postaci x,y,z dzielac zawartosc pliku po ;
            string_from_list_of_points = content_of_file_of_points.split(";")
            #Dla kazdego stringa z listy sprawdzam dziele go na liste wspolrzednych i sprawdzam czy kazda ze wspolrzednych
            #jest faktycznie liczba uzywajac funkcji is_valid_index_of_point. Jesli ktoras nie jest to ignoruje punkt
            for point in string_from_list_of_points:
                index_of_point = point.split(",")
                if is_valid_index_of_point(index_of_point):
                    local_list_of_points = np.append(local_list_of_points, np.array([list(map(int, index_of_point))]), axis=0)
                else:
                    continue
        #przypisuje do globalnej listy punktow lokalna z fukcji.
        points_from_file = local_list_of_points

#Funkcja podpieta do przycisku Przelicz, ktora liczy nowy diagram dla zestawu punktow z pliku
def recalculate_for_new_set_of_points():
    draw_voronoi3d_diagram(points_from_file)

#Funkcja generuje pusta tablice 3d zawierajca punkty od ktorych liczone byly obszary w diagramie
def table_for_points(points):
    #tworzenie pustej tablicy 3d
    table_of_points = np.zeros([size_of_diagram, size_of_diagram, size_of_diagram], np.int)
    #wpisywanie punktow z listy punktow na pusta tablice 3d
    for point in points:
        table_of_points[[point[0]], [point[1]], [point[2]]] = True
    return table_of_points

#Funkcja ktora zmienia diagram z obszarami dla kazdego punktu na raz na liste list zawierajacych indeks punktu w tablicy
#ktory jest tez oznaczeniem obszaru w tablicy3d i tablice 3d z zaznaczonym obszarem dla danego punktu
#Tablica z zaznaczonym obszarem dla punktu jest teraz tablica zero jedynkowa
def table_of_areas_for_points(list_of_points, voronoi_table):
    #lista zawierajca indeksy punktow
    list_of_points = list(range(1, np.shape(list_of_points)[0] + 1))
    list_of_area_matrix = []
#W petli tam gdzie w tablicy jest obszar o indeksie x jest wpisywane 1, tam gdzie jest cokolwiek innego jest 1
    for indexOfPoint in list_of_points:
        area_matrix_for_one_color = np.zeros(voronoi_table.shape, np.int)
        area_matrix_for_one_color[np.nonzero(voronoi_table == indexOfPoint)] = 1
        list_of_area_matrix.append([indexOfPoint, area_matrix_for_one_color])
    return list_of_area_matrix

#Rysowanie diagramu Voronoi
def draw_voronoi3d_diagram(points):
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    #Rysowanie obszaru dla kazdego punktu w innym kolorze
    #Zmieniam tablice 3d z jednej gdzie obszar oznaczany jest indeksem punktu na liscie na liste tablic zero jedynkowych
    #Na liste list [indeks punktu w tablicy, tablica zero jedynkowa gdzie jest dany indeks]
    #poniewaz funkcja voxels koloruje dla wartosci innych od zera na dany kolor
    for area in table_of_areas_for_points(points, Voronoi3D(points)):
        #Generowanie losowego transparentnego koloru
        random_color_hex = '#' + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + "30"
        #Rysowanie obszaru na wykresie3d voxelami
        ax.voxels(area[1], facecolors=random_color_hex, edgecolors=None, shade=False)
    #Dodanie do wykresu punktow od ktorych liczone byly wykresy
    ax.voxels(table_for_points(points), facecolor='black', edgecolors='black', shade=False)

    canvas.get_tk_widget().place(x=150, y=5)
    return canvas


#GUI ustawienia ogolne
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