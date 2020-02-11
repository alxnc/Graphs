#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graphs - Draws a graph from given equation.

This is a conversion of my old program created at college at 2002y. 
Just to learn python at 2020y.

"""

OPERS = "+-*/^"

import math 

#math.radians() - > ze stopni na raniany /

fx = [] #for function values 


def checkBrackets(sFun):
    """
     Function checks for brackets in string
     i: string with function
     r: 0 -> no brackets / 1 -> brackets ok / -1 -> brackets not ok
    """
    obr = 0 # int open brackets counter
    cbr = 0 # int closing brackets counter
    wynik = 0 # int result of scan

    if "(" or ")" in sFun:
        for x in sFun:
            if x == "(":
                obr += 1
                wynik = 1
                continue
            elif x == ")":
                cbr += 1
                continue

    if(obr != cbr): wynik = -1
    return wynik

def analizeOperations(sFun):
    """
     Function checks if there are two operators one after the other
     i: string with function
     r: true if ok / false when err
    """
    ok = True # returning var
    sFun.replace(" ","")
    for i in range(len(sFun)):
        if sFun[i] in OPERS:
            if i>=1:
                if sFun[i-1] in OPERS:
                    #two opers side by side
                    ok = False
    return ok    



func = "sin+20+2"
print(checkBrackets(func))
print(analizeOperations(func))