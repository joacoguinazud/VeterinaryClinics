#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 17:17:14 2024

@author: joaquingd
"""

import pandas as pd
import haversine as hs

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
        return self.lista_objetos(self.B), self.distancia(self.B)
    
    def completar(self, S):
        if len(S) == len(self.clinicas):
            if self.costo(S) <= self.presupuesto and self.distancia(S) > self.distancia(self.B):
                #Es un candidato si no supera el presupuesto y tiene mayor distancia al anterior
                self.B = S.copy()
        else:
            self.completar(S + [1])
            self.completar(S + [0])
            
    def distancia(self, candidata):
        ret = self.lista_objetos(candidata)
        dist = 0
        #Iteramos sobre todos los pares posibles en nuestra lista candidate
        for i in ret:
            for j in ret:
                #No nos preocupamos cuando i = j porque la distancia Haversine dará 0
                lugar1 = [i.latitud, i.longitud]
                lugar2 = [j.latitud, j.longitud]
                dist += hs.haversine(lugar1, lugar2)
        #Dividimos por 2 porque hay distancias repetidas
        return dist/2
    
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

tp = pd.read_csv("ta_datos_tp.csv")
c = []

for i in range(len(tp)):
    c = c + [Clinica(tp.iloc[i, :])]

ret, d_l = Veterinaria(c, 5000000).resolver()

import unittest

class TestVeterinaria(unittest.TestCase):

    tp = pd.read_csv("ta_datos_tp.csv")
    c = []

    for i in range(len(tp)):
        c = c + [Clinica(tp.iloc[i, :])]
                
    def test_sinclinicas(self):
        self.assertEqual( Veterinaria([], 5000000).resolver(), ([], 0.0) )
                
    def test_ningunaentra(self):
        self.assertEqual( Veterinaria(self.c, 100000).resolver(), ([], 0.0) )
        
    def test_dosclinicas(self):
        self.assertEqual( Veterinaria(self.c, 850000).resolver(), ([self.c[1], self.c[2]], 0.5994317873370845) )
    
    #Si corren este test esten advertidos que dura 50 minutos
    def test_entrantodas(self):
        self.assertEqual( Veterinaria(self.c, 17000000).resolver(), (self.c, 618.340926884364) )

unittest.main()