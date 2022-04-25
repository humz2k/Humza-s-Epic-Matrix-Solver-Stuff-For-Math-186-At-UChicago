import numpy as np
from enum import Enum
from copy import deepcopy
import itertools

i = 1.j

T = "T"

t = "t"

letters = "abcdefghijklmnopqrstuvwxyz"
letters += letters.upper()

var = Enum('var',list(letters))

def det(m):
    return np.linalg.det(m.array)

def eigenvalues(m,precision=10):
    return np.around(np.linalg.eigvals(m.array),precision)

def eigenvectors(m,precision=10):
    vals = eigenvalues(m)
    dim = list(set(list(m.array.shape)))
    assert len(dim) == 1
    dim = dim[0]
    coords = np.array([[0] * dim] * dim)
    for j in range(dim):
        coords[j][j] = 1
    for j in vals:
        temp = matrix(m.array - np.identity(dim) * j)
        for k in coords:
            coord = matrix(np.array([k]).T)
            print(temp * coord)


        #print(np.linalg.solve(temp,)

def str_complex(k,precision=3):
    real = np.real(k)
    complex = (k-real)*(-i)
    if complex == 0:
        return ("{:."+str(precision)+"g}").format(real)
    if real == 0:
        if complex == 1:
            return "i"
        elif complex == -1:
            return "-i"
        return ("{:."+str(precision)+"g}").format(complex) + "i"
    return ("{:."+str(precision)+"g}").format(real) + "+" + ("{:."+str(precision)+"g}").format(complex) + "i"

class sig:
    def __init__(self,vars,expr):
        ranges = (range(j[0],j[1]+1) for j in vars.values())
        self.indexes = list(itertools.product(*ranges))
        self.values = []
        for j in self.indexes:
            self.values.append(expr(*j))

    def solve(self,value=None):
        if value == None:
            assert len(self.values[0].scalers) == 0
            out = np.zeros_like(self.values[0].array)
            for j in self.values:
                out += j.array
            return matrix(out)
        else:
            assert len(self.values[0].scalers) == 1
            values = []
            for j in self.values:
                values.append(j.array.flatten())
            values = np.array(values)
            vals = {}
            for key,val in zip(self.indexes,np.linalg.solve(values,value.array.flatten())):
                vals[key] = val
            self.values[0].scalers[0].const.vals = vals
            return self.values[0].scalers[0].const

class expr:
    def __init__(self,expr):
        self.expr = expr.expr

        self.scaler = 1
        self.scaler_var = None

        def traverse(t):
            out = []
            for i in t:
                if isinstance(i,var):
                    out.append(i)
                if isinstance(i,expr_object):
                    if isinstance(i.var,list):
                        out += i.var
                    else:
                        out.append(i.var)
            for i in t:
                if isinstance(i,list):
                    out += traverse(i)
            return out

        self.vars = list(set(traverse(self.expr)))

    def __mul__(self,other):
        if isinstance(other,constant):
            self.scaler_var = other
        else:
            self.scaler *= other
        return self

    def __call__(self,*args):
        vals = {}
        for key,value in zip(self.vars,args):
            vals[key] = value
        out = deepcopy(self.expr)
        def traverse(t,index):
            for j in t:
                if isinstance(j,var):
                    test = out
                    for k in index[:-1]:
                        test = test[k]
                    test[index[-1]] = vals[j]
                if isinstance(j,expr_object):
                    if isinstance(j.var,list):
                        test = out
                        for k in index[:-1]:
                            test = test[k]
                        test[index[-1]] = j.func(*[vals[l] for l in j.var])
                    else:
                        test = out
                        for k in index[:-1]:
                            test = test[k]
                        test[index[-1]] = j.func(vals[j.var])
                if isinstance(j,list):
                    traverse(j,index + [0])
                index[-1] += 1
        traverse(out,[0])

        def traverse2(t):
            count = 0
            for idx,j in enumerate(t):
                exists = False
                if isinstance(j, list):
                    for k in j:
                        if isinstance(k, list):
                            exists = True
                            break
                    if exists:
                        count += traverse2(j)
                    else:
                        if isinstance(j[0],expr_constant) or isinstance(j[2],expr_constant):
                            pass
                        else:
                            count += 1
                            if j[1] == "^":
                                t[idx] = j[0] ^ j[2]
                            if j[1] == "*":
                                t[idx] = j[0] * j[2]
                            if j[1] == "+":
                                t[idx] = j[0] + j[2]
                            if j[1] == "-":
                                t[idx] = j[0] - j[2]
                            if j[1] == "**":
                                t[idx] = j[0] ** j[2]
            return count

        while traverse2(out) != 0:
            pass
        if self.scaler_var != None:
            out[0].scalers.append(self.scaler_var([vals[k] for k in self.scaler_var.vars]))
        out[0].array *= self.scaler
        return out[0]

def new_expr():
    temp = expr_object(None,None)
    temp.expr = []
    return temp

class expr_object:
    def __init__(self,func,var,op=None):
        self.func = func
        self.var = var
        self.op = op
        self.expr = [self]

    def __rshift__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + other.expr]
        else:
            self.expr = [self.expr + [other]]
        return self

    def __mul__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + ["*"] + other.expr]
        else:
            self.expr = [self.expr + ["*"] + [other]]
        return self

    def __add__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + ["+"] + other.expr]
        else:
            self.expr = [self.expr + ["+"] + [other]]
        return self

    def __sub__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + ["-"] + other.expr]
        else:
            self.expr = [self.expr + ["-"] + [other]]
        return self

    def __pow__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + ["**"] + other.expr]
        else:
            self.expr = [self.expr + ["**"] + [other]]
        return self

    def __xor__(self,other):
        if isinstance(other,expr_object):
            self.expr = [self.expr + ["^"] + other.expr]
        else:
            self.expr = [self.expr + ["^"] + [other]]
        return self

class miter:
    def __init__(self,name,vals={}):
        self.vals = vals
        self.name = name
    def __call__(self,idx):
        if isinstance(idx,var):
            return expr_object(self,idx)
        return self.vals[idx]
    def __str__(self):
        return self.name.name

class expr_constant:
    def __init__(self,const,*args):
        self.const,self.args = const,args
        try:
            self.val = self.const.val(*self.args)
        except:
            self.val = None

    def __call__(self):
        return self.const.val(*self.args)

    def __str__(self):
        val = ""
        try:
            val = "=" + str_complex(self.const.val(*self.args))
        except:
            pass
        return self.const.name.name + "(" + ",".join([str(j) for j in self.args]) + ")" + val

class constant:
    def __init__(self,name,vars=None,vals={}):
        self.name = name
        self.vars = vars
        self.vals = vals

    def __str__(self):
        return self.name.name + "(" + ",".join([j.name for j in self.vars]) + ")"

    def __call__(self,*args):
        return expr_constant(self,*args)

    def print_vals(self):
        for key in self.vals.keys():
            print(expr_constant(self,*key))

    def val(self,*args):
        return self.vals[tuple(args)]

    def expr(self):
        return expr_object(self,self.vars)

def bracket(v1,v2):
    return (v1^t) * v2

class matrix:
    def __init__(self,array,print_precision=3):
        self.array = np.array(array)
        self.shape = self.array.shape
        self.print_precision = print_precision
        self.scalers = []

    def dot(self,other):
        if len(self.array.shape) == 2:
            assert self.array.shape == other.array.shape
            if self.array.shape[1] == 1 or self.array.shape[0] == 1:
                return np.dot(self.array.flatten(),other.array.flatten())
        raise Exception("Cant dot")

    def __pow__(self,other):
        if other == -1:
            return matrix(np.linalg.inv(self.array),print_precision=self.print_precision)
        else:
            if other > 0:
                out = self.array
                for j in range(other-1):
                    out = np.matmul(out,out)
                return matrix(out,print_precision = self.print_precision)
        raise Exception("NOT IMPLEMENTED")

    def __add__(self,other):
        return matrix(self.array + other.array,print_precision=self.print_precision)

    def __sub__(self,other):
        return matrix(self.array - other.array,print_precision=self.print_precision)

    def __mul__(self,other):
        return matrix(np.matmul(self.array,other.array),print_precision=self.print_precision)

    def __xor__(self, other):
        if other == T:
            return matrix(self.array.T,print_precision=self.print_precision)
        if other == t:
            return matrix(self.array.conj().T,print_precision=self.print_precision)
        if other == -1:
            return matrix(np.linalg.inv(self.array),print_precision=self.print_precision)

    def __str__(self):
        real = np.real(self.array)
        complex = np.real((self.array - real) * -i)
        longest = 0
        out = []
        for row in range(self.array.shape[0]):
            temp_out = []
            for column in range(self.array.shape[1]):
                real_part = real[row][column]
                complex_part = complex[row][column]
                if complex_part == 0:
                    temp_out.append(("{:."+str(self.print_precision)+"g}").format(real_part))
                else:
                    if real_part == 0:
                        if complex_part == 1:
                            temp_out.append("i")
                        elif complex_part == -1:
                            temp_out.append("-i")
                        else:
                            temp_out.append(("{:."+str(self.print_precision)+"g}i").format(complex_part))
                    else:
                        if complex_part == 1:
                            temp_out.append(("{:."+str(self.print_precision)+"g}+i").format(real_part))
                        elif complex_part == -1:
                            temp_out.append(("{:."+str(self.print_precision)+"g}-i").format(real_part))
                        else:
                            temp_out.append(("{:."+str(self.print_precision)+"g}+{:."+str(self.print_precision)+"g}i").format(real_part,complex_part))
                if len(temp_out[-1]) > longest:
                    longest = len(temp_out[-1])
            out.append(temp_out)
        outstring = "["
        middle = len(out)//2
        for idx,row in enumerate(out):
            if idx != 0:
                outstring += " "
            outstring += "[" + ((" {:<"+str(longest)+"} ")* len(row)).format(*row) + "]\n"
            if idx == middle:
                if len(self.scalers) != 0:
                    outstring = outstring[:-1]
                    for k in self.scalers:
                        outstring += " * " + str(k)
                    outstring += "\n"
        outstring = outstring[:-1]
        outstring += "]"
        return outstring
