import tkinter as tk
from tkinter import filedialog as fd
from math import sqrt
import numpy as np
from matplotlib.figure import Figure
import random
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#3D:
#Początkowy zestaw punktow do Voronoi3D:
rozmiar_diagramu = 30
lista_punktow = [0,0,0]
sites = [[0, 0, 0], [rozmiar_diagramu - 1, rozmiar_diagramu - 1, rozmiar_diagramu - 1], [rozmiar_diagramu - 1, 0, 0]]


def mojVoronoi3DTest(punkty):
    global rozmiar_diagramu
    tablica = np.zeros([rozmiar_diagramu, rozmiar_diagramu, rozmiar_diagramu], np.int)

    for colin, col in enumerate(tablica):
        for rowin, row in enumerate(col):
            for tabin, tab in enumerate(row):
                obecny_dystans = rozmiar_diagramu*rozmiar_diagramu*rozmiar_diagramu
                obecny_site = "X"
                for pin, pix in enumerate(punkty):
                    dystans = dystans3d(colin, rowin, tabin, pix[0], pix[1], pix[2])
                    if obecny_dystans > dystans:
                        obecny_dystans = dystans
                        obecny_site = pin+1
                tablica[colin][rowin][tabin] = obecny_site
    return tablica

def SprawdzCzyPunkt(punkt):
    for wsp in punkt:
        if not wsp.isdigit():
            return False
    return True

def dystans3d(x1,y1,z1,x2,y2,z2):
    distance = sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    return distance

def WczytajPlik():
    global lista_punktow
    lokalna_lista_punktow = np.empty((0,3), int)
    nazwapliku = fd.askopenfilename(initialdir=".", title="Select file",filetype=(("Text file","*.txt"),("All files","*.*")) )
    if nazwapliku:
        with open(nazwapliku,"r") as f:
            tresc_pliku_z_punktem = "".join(f.read().split())
            lista_punktow_str = tresc_pliku_z_punktem.split(";")
            for punkt in lista_punktow_str:
                wspolrzedne_punktu_do_listy = punkt.split(",")
                if (SprawdzCzyPunkt(wspolrzedne_punktu_do_listy)):
                    lokalna_lista_punktow = np.append(lokalna_lista_punktow,np.array([list(map(int, wspolrzedne_punktu_do_listy))]),axis=0)
                else:
                    continue
        lista_punktow = lokalna_lista_punktow

def PrzeliczDlaNowegoZestawuPunktow():
    global lista_punktow
    NarysujDiagramVoronoi3D(lista_punktow)

def TablicaPunktow(punkty):
    global rozmiar_diagramu
    tablicaPunktow = np.zeros([rozmiar_diagramu, rozmiar_diagramu, rozmiar_diagramu], np.int)
    for punkt in punkty:
        tablicaPunktow[[punkt[0]],[punkt[1]],[punkt[2]]]=True
    return tablicaPunktow

def TablicaObszarowDlaPunktu(punkty,MacierzVoronoi):
    wartosci = list(range(1, np.shape(punkty)[0]+1))
    lista_macierzy_kolorow = []
    for wartosc in wartosci:
        MacierzPrzestrzeniDlaPojedynczegoPunktu = np.zeros(MacierzVoronoi.shape, np.int)
        MacierzPrzestrzeniDlaPojedynczegoPunktu[np.nonzero(MacierzVoronoi == wartosc)] = 1
        lista_macierzy_kolorow.append([wartosc, MacierzPrzestrzeniDlaPojedynczegoPunktu])
    return lista_macierzy_kolorow

def NarysujDiagramVoronoi3D(sites):
    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    ax = fig.add_subplot(1, 1, 1, projection="3d")
    for obszar in TablicaObszarowDlaPunktu(sites, mojVoronoi3DTest(sites)):
        losowy_kolor = '#' + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') + format(random.randint(17, 255), 'x') +"30"
        print(losowy_kolor)
        ax.voxels(obszar[1], facecolors=losowy_kolor, edgecolors=None, shade=False)
    ax.voxels(TablicaPunktow(sites), facecolor='black', edgecolors='black', shade=False)

    canvas.get_tk_widget().place(x=150, y=5)
    return canvas

#Ogolne
root = tk.Tk()
root.geometry("660x500")
root.wm_title("Voronoi3D")
root.resizable(False, False)

#Definiowanie elementow GUI
Wczytaj_Przycisk = tk.Button(root, text = "Wczytaj punkty z pliku", command=WczytajPlik, height=1,width=18)
Przelicz_Przycisk = tk.Button(root, text = "Przelicz", command=PrzeliczDlaNowegoZestawuPunktow, height=1,width=18)

#Rysowanie wykresu 3D Voronoi
canvas = NarysujDiagramVoronoi3D(sites)
toolbar = NavigationToolbar2Tk(canvas, root)

#Pozycjonowanie elementow GUI
Wczytaj_Przycisk.place(x = 5,y = 5)
Przelicz_Przycisk.place(x = 5,y = 35)
toolbar.update()
root.mainloop()