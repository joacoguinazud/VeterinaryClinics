import pandas as pd
import haversine as hs
from scipy.spatial import ConvexHull
import numpy as np

class Veterinaria:

    B = []
    clinicas = []
    presupuesto = 0
    
    def __init__(self, cli, p):
        self.clinicas = cli
        self.presupuesto = p
        
    def resolver(self):
        self.B = []
        self.completar([])
        return self.lista_objetos(self.B)
    
    def completar(self, S):
        if len(S) == len(self.clinicas):
            if self.costo(S) <= self.presupuesto and self.area_poligono(S) > self.area_poligono(self.B):
                self.B = S.copy()
        else:
            self.completar(S + [1])
            self.completar(S + [0])

    def area_poligono(self, candidata):
        """Calcula el área del polígono convexo que forman las clínicas seleccionadas."""
        ret = self.lista_objetos(candidata)
        if len(ret) < 3:  # Se necesitan al menos 3 clínicas para formar un polígono
            return 0
        puntos = np.array([[clinica.latitud, clinica.longitud] for clinica in ret])
        hull = ConvexHull(puntos)  # Calcula el polígono convexo
        return hull.area  # Devuelve el área del casco convexo
    
    def costo(self, candidata):
        ret = 0
        for i in range(len(candidata)):
            if candidata[i] == 1:
                ret += self.clinicas[i].costo
        return ret
    
    def lista_objetos(self, candidata):
        ret = []
        for i in range(len(candidata)):
            if candidata[i] == 1:
                ret = ret + [self.clinicas[i]]
        return ret

class Clinica:

    nombre = ""
    latitud = 0
    longitud = 0
    costo = 0
    
    def __init__(self, clinic):
        self.nombre = clinic["Nombre"]
        self.latitud = clinic["Latitud"]
        self.longitud = clinic["Longitud"]
        self.costo = clinic["Costo"]
    
    def __repr__(self):
        return self.nombre

# Lectura de datos de ejemplo
tp = pd.read_csv("ta_datos_tp.csv")
c = []

for i in range(len(tp)):
    c = c + [Clinica(tp.iloc[i, :])]

# Resolución del problema maximizando el área del casco convexo
Veterinaria(c, 5000000).resolver()

#[Colegiales I,
#Colegiales II,
#Coghlan III,
#Núñez I,
#Núñez IV,
#Palermo II,
#Palermo III,
#Palermo IV,
#Palermo V]

import unittest

class TestVeterinaria(unittest.TestCase):

    tp = pd.read_csv("taa_datos_tp.csv")
    c = []

    for i in range(len(tp)):
        c = c + [Clinica(tp.iloc[i, :])]
                
    def test_sinclinicas(self):
        self.assertEqual(Veterinaria([], 5000000).resolver(), [])
                
    def test_ningunaentra(self):
        self.assertEqual(Veterinaria(self.c, 100000).resolver(), [])
        
    def test_dosclinicas(self):
        self.assertEqual(Veterinaria(self.c, 850000).resolver(), [self.c[1], self.c[2]])

    def test_entrantodos(self):
        self.assertEqual(Veterinaria(self.c, 17000000).resolver(), self.c)

unittest.main()
