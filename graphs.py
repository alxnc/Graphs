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
from itertools import tee, groupby

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

def check_brackets(fun):
    """
     Function checks brackets in string
     fun: string with function
     returns: 0 -> brackets failure / 1 -> brackets ok 
    """
    open_brackets = 0
    for c in fun:
        if c == "(":
            open_brackets += 1
        elif c == ")":
            if open_brackets:
                open_brackets -= 1
            else:
                return False
    return open_brackets == 0

def old_check_dbl_operators(fun):
    """
     Function checks if there are two operators one after the other
     fun: string with function
     returns: true if ok / false when err
    """        
    for i in range(1,len(fun)):
        if fun[i] in OPERS:
                if fun[i-1] in OPERS:
                    #two opers side by side
                    return False
    return True    

def check_dbl_operators(fun):
    """
     Function checks if there are two operators one after the other
     s: string with function
     returns: true if ok / false when err
    """
    is_oper = map(lambda x: x in OPERS, fun)
    return all(len(list(group)) == 1 for x, group in groupby(is_oper) if x)    

def old_check_op_after_cb(fun):
    """
     Function checks if there is operator after closing bracket
     i: string with function
     r: true if ok / false when err
    """
    for i in range(len(fun)-1):
        if fun[i] == ")" and (fun[i+1] != ")"
                            and not fun[i+1] in OPERS):
                            return False
    return True    

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def check_op_after_cb(fun):
    """
     Function checks if there is operator after closing bracket
     fun: string with function
     returns: true if ok / false when err
    """
    for c1, c2 in pairwise(fun):
        if (c1 == ")" 
            and c2 not in OPERS 
            and c2 != ")"):
            return False
    return True

def to_RPN(fun,x_val):
    """
    Function convert infix string to RPN
    i: string with function infix
    r: RPN[] 
    """
    stos = []       #stack
    wyjscie = []    #exit string

    index = 0
    while index < len(fun):
        expr = fun[index:]
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
        if fun[index] == "(":                  #if "(" put on stos
            stos.append(fun[index])
            index += 1
            continue
        if fun[index] == ")":                  
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
        if fun[index].lower() == "x":                  #insert x value on wyjscie
            wyjscie.append(float(x_val))
            index += 1
            continue        
        if fun[index] in OPERS:        
            if index == 0:                  #if this is first char of string insert 0.0 before it
                wyjscie.append(0.0)
            elif fun[index-1] == "(":
                wyjscie.append(0.0)         #if operator is after openning bracket insert 0.0 before it
            if not stos:                        #if stos is empty insert operator
                stos.append(fun[index])               
                index += 1
                continue
            if OP_PRIO[fun[index]] > OP_PRIO[stos[-1]]:    #if oper in fun has higher prio add it to stos
                stos.append(fun[index])
                index += 1
                continue            
            else:                                               
                while len(stos):                                #if oper in fun has prio <= oper in stos
                                                                #move all opers from stos to wyjscie with prio >= oper                     
                    if (OP_PRIO[stos[-1]]>OP_PRIO[fun[index]]
                        or (
                            OP_PRIO[stos[-1]] == (OP_PRIO[fun[index]] 
                            and OP_PRIO[fun[index]]<3)
                        )
                    ): 
                        wyjscie.append(stos[-1])
                        del stos[-1]
                    else: break
                stos.append(fun[index])
                index += 1                
    # move stos to wyjscie LIFO
    while len(stos):
        if stos[-1] not in ["(",")",]:
            wyjscie.append(stos[-1])
        del stos[-1]
    return wyjscie

def eval_expr(fun, x_val = 1):
    """
    Function evaluate RPN string 
    i: string with function infix 
    r: value
    """   
    #check string
    if not check_brackets(fun):
        raise SyntaxError("The expression have unclosed brackets!")
    elif not check_dbl_operators(fun):      
        raise SyntaxError("The expression have incorrectly written operators!")
    elif not check_op_after_cb(fun):
        raise SyntaxError("Missing operator after closing bracket!")
    
    stack = [] 
    for x in to_RPN(fun, x_val):
        if isinstance(x, float):
            stack.append(x)
        elif x in OPERS:
            b, a = stack.pop(), stack.pop()
            stack.append(OPERS[x](a, b))
        elif x in FUNCTIONS:
            stack.append(FUNCTIONS[x](stack.pop()))
    if len(stack) != 1:
        raise SyntaxError("More than one value remains on stack")
    return round(stack[0], DEC_PLACES)        #return rounded result
    
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
            print("{0} = {1}".format(expr,eval_expr(expr,x_val)))
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
                y.append(eval_expr(expr, i))
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
        print("{0} = {1}".format(expr,eval_expr(expr)))

if __name__ == "__main__":
  main()