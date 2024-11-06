#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:13:47 2024

@author: joaquingd
"""

import pandas as pd
import haversine as hs

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
    
    #Definimos una forma de poder ordenar objetos de la clase Clinica por costo
    def __lt__(self, other):
        return self.costo < other.costo

def veterinaria(clinicas, presupuesto):
    #Ordenamos de menor a mayor
    clinicas.sort()
    pre = presupuesto
    ret = []
    
    for i in clinicas:
        pre -= i.costo
        #Mientras no se supere el presupuesto, seguir añadiendo clínicas
        if pre >= 0:
            ret = ret + [i]
        else:
            break
    
    #Calculamos la distancia como en backtracking
    dist = 0
    for i in ret:
        for j in ret:
            lugar1 = [i.latitud, i.longitud]
            lugar2 = [j.latitud, j.longitud]
            dist += hs.haversine(lugar1, lugar2)
    d_l = dist/2
    
    return ret, d_l

tp = pd.read_csv("ta_datos_tp.csv")
c = []

for i in range(len(tp)):
    c = c + [Clinica(tp.iloc[i, :])]

ret, d_l = veterinaria(c, 5000000)