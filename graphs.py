#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Graphs - Calculate expression or draws a graph from given equation.

This is a conversion of my old program created at college at 2002y. 
Just to learn python at 2020y.

"""

import re
import operator
import math 
import matplotlib.pyplot as plt

DEC_PLACES = 3      #number of decimal places after rounding

FUNCTIONS = {
    'sin': lambda x:math.sin(math.radians(x)),
    'cos': lambda x:math.cos(math.radians(x)),
    'tan': lambda x:math.tan(math.radians(x)),
    'ln': lambda x:math.log(x),
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
'(?:[a-z]{2,}[(])'
)

def checkBrackets(sFun):
    """
     Function checks brackets in string
     i: string with function
     r: 0 -> brackets failure / 1 -> brackets ok 
    """

    wynik = 0 # int result of scan

    if "(" or ")" in sFun:
        for x in sFun:
            if x == "(":
                wynik += 1
                continue
            elif x == ")":
                wynik -= 1
                continue

    if(wynik != 0): wynik = 0
    else: wynik = 1
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
                    break
    return ok    

def analizeOpAfterCB(sFun):
    """
     Function checks if there is operator after closing bracket
     i: string with function
     r: true if ok / false when err
    """
    ok = True # returning var
    sFun.replace(" ","")
    for i in range(len(sFun)):
        if sFun[i] == ")" and (i+1)<len(sFun):
            if sFun[i+1] != ")":
                if not sFun[i+1] in OPERS:
                    #missing operator after closing bracket
                    ok = False
                    break
    return ok    

def toRPN(sFun,x_val):
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
            if index == 0:                  #if this is first char of string insert 0.0 before it
                wyjscie.append(0.0)
            elif sFun[index-1] == "(":
                wyjscie.append(0.0)         #if operator is after openning bracket insert 0.0 before it
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

def evalExpr(sFun, x_val = 1):
    """
    Function evaluate RPN string 
    i: string with function infix 
    r: value
    """
    stos = [] #stack
    #check string
    if not checkBrackets(sFun):
        raise SyntaxError("The expression have unclosed brackets!")
    elif not analizeOperations(sFun):      
        raise SyntaxError("The expression have incorrectly written operators!")
    elif not analizeOpAfterCB(sFun):
        raise SyntaxError("Missing operator after closing bracket!")
    else:
        sRPN = toRPN(sFun,x_val)
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
        return round(stos[0],DEC_PLACES)        #return rounded result
    
def showHelp():
    print("Allowed operators and functions:")
    print("+-*/^")
    print("sin, cos, tan, ln")
    print("You can enter arithmetic expressions like:")
    print("2*(3-4)^2")
    print("2*sin(30-4*2)")
    print("or functions like:")
    print("2*x^2+3*x+1")
    print("2*sin(x)*x+1")

def main():    
    expr = input("Enter an arithmetic expression (type help for info):")    
    if expr.lower() == "help":
        showHelp()
        exit()
    if "x" in expr:
        option = input("Expression cotains 'x' variable, enter 'r' for range or 'v' for value:")
        while option.lower() != 'r' and option.lower() != 'v':
            option = input("Expression cotains 'x' variable, enter 'r' for range or 'v' for value:")
        if option == 'v':
            x_val = ''
            while not isinstance(x_val,float):
                try:
                    x_val = float(input("Enter x value:"))
                except:
                    print("That was no valid number.")
            print("{0} = {1}".format(expr,evalExpr(expr,x_val)))
        else:
            x_val = ''
            x_start = ''
            x_end = ''
            x_step = ''
            while (not isinstance(x_start,float) 
                    and not isinstance(x_end,float)
                    and not isinstance(x_step,float)
                ):
                try:
                    x_start, x_end, x_step = map(float,input("Enter start value, end value and step for range (eg.: 0,5,1): ").split(","))
                except:
                    print("That was no valid number.")
            #make a graph
            x = []
            y = []
            #calculating values
            i = x_start
            while i <= x_end:
                x.append(i)
                y.append(evalExpr(expr, i))
                i += x_step
            # plotting the points  
            plt.plot(x, y) 
            # naming the x axis 
            plt.xlabel('x') 
            # naming the y axis 
            plt.ylabel('f(x)') 
            # giving a title to my graph 
            expr += F"\n in range {x_start} to {x_end} step {x_step}"
            plt.title(expr)   
            # function to show the plot 
            plt.show() 
    else:
        print("{0} = {1}".format(expr,evalExpr(expr)))

if __name__ == "__main__":
  main()