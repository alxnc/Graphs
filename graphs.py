#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graphs - Draws a graph from given equation.

This is a conversion of my old program created at college at 2002y. 
Just to learn python at 2020y.

"""

import re
#import time
import operator
import math 

FUNCTIONS = {
    'sin': lambda x:math.sin(math.radians(x)),
    'cos': lambda x:math.cos(math.radians(x)),
}

OPERS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,    
}

OP_PRIO = {
    '(':0,
    '+':1,
    '-':1,
    ')':1,
    '*':2,
    '/':2,
    '^':3,
}

NUM_MATCH = re.compile(
'(?:[1-9][0-9]*|0)'
'(?:[.][0-9]+)?'
)

FUN_MATCH = re.compile(
'(?:[a-z]{1,}[(])'
)

x_val = 1           #for tests only

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



def toRPN(sFun):
    """
    Function convert infix string to RPN
    i: string with function infix
    r: RPN[] 
    """
    stos = []       #stack
    wyjscie = []    #exit string

    index = 0
    while index < len(sFun):
        expr = sFun[index:]
        is_num = NUM_MATCH.match(expr)
        is_fun = FUN_MATCH.match(expr)          
        if is_num:                              #if num put on wyjscie
            num = is_num.group(0)
            wyjscie.append(float(num))            
            index += len(num)
            continue            
        if is_fun:                              #if function put on stos
            fun = is_fun.group(0)
            fun = fun[:-1]                      #remove "("
            if fun in FUNCTIONS:
                stos.append(fun)
                index += len(fun)
                continue                
            else:
                raise("Błąd! Nieznana funkcja.")
        if sFun[index] == "(":                  #if "(" put on stos
            stos.append(sFun[index])
            index += 1
            continue
        if sFun[index] == ")":                  
            for i in range(len(stos)-1,0,-1):   #if ")" move all operands till "(" to wyjscie LIFO
                if stos[i] == "(":
                    del stos[i]
                    if stos[i-1] in FUNCTIONS:
                        wyjscie.append(stos[i-1])
                        del stos[i-1]
                    break
                else:
                    wyjscie.append(stos[i])
                    del stos[i]                
            index += 1
            continue
        if sFun[index].lower() == "x":                  #insert x value on wyjscie
            wyjscie.append(float(x_val))
            index += 1
            continue        
        if sFun[index] in OPERS:                
            if not stos:                        #if stos is empty insert operator
                stos.append(sFun[index])
                index += 1
                continue
            if OP_PRIO[sFun[index]] > OP_PRIO[stos[-1]]:    #if oper in sFun has higher prio add it to stos
                stos.append(sFun[index])
                index += 1
                continue            
            else:                                               
                while len(stos):                                #if oper in sFun has prio <= oper in stos
                                                                #move all opers from stos to wyjscie with prio >= oper                     
                    if (OP_PRIO[stos[-1]]>OP_PRIO[sFun[index]]
                        or (
                            OP_PRIO[stos[-1]] == (OP_PRIO[sFun[index]] 
                            and OP_PRIO[sFun[index]]<3)
                        )
                    ): 
                        wyjscie.append(stos[-1])
                        del stos[-1]
                    else: break
                stos.append(sFun[index])
                index += 1                
    # move stos to wyjscie LIFO
    while len(stos):
        if stos[-1] not in ["(",")",]:
            wyjscie.append(stos[-1])
        del stos[-1]
    return wyjscie

def evalRPN(sRPN):
    """
    Function evaluate RPN string 
    i: RPN string 
    r: value
    """
    stos = [] #stack
    while len(sRPN):        
        if isinstance(sRPN[0],float):
            stos.append(sRPN[0])
            del sRPN[0]
            continue
        if sRPN[0] in OPERS:
            func = OPERS[sRPN[0]]           #get function for oper
            val = func(stos[-2],stos[-1])                
            del stos[-2:]                   #remove used vals from stos
            del sRPN[0]                     
            stos.append(val)
            continue
        if sRPN[0] in FUNCTIONS:
            func = FUNCTIONS[sRPN[0]]           #get function 
            val = func(stos[-1])                
            del stos[-1]                   #remove used vals from stos
            del sRPN[0]                     
            stos.append(val)
            continue    
    return stos[0] #return result

func = "sin(2*x+28)+12+2*(3*4+10/5)"


#print(checkBrackets(func))
#print(analizeOperations(func))
RPNlist=toRPN(func)
print(evalRPN(RPNlist))

print(evalRPN(toRPN("3^3^2")))

