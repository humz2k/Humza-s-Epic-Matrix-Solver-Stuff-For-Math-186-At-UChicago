from sympy import *

class Matrix(Matrix):
    def to(self,space):
        pass

class VectorSpace:
    def __init__(self,basis=None):
        self.basis = basis

    def verifybasis(self):
        var_strings = list("abcdefghjklmnopqrstuvwxyz"[:len(self.basis)])
        v1_vars = symbols("1 ".join(var_strings) + "1 ")
        v2_vars = symbols("2 ".join(var_strings) + "2 ")
        v3_vars = symbols("3 ".join(var_strings) + "3 ")

        v1 = sum([i*j for i,j in zip(v1_vars,self.basis)],zeros(len(self.basis),1))
        v2 = sum([i*j for i,j in zip(v2_vars,self.basis)],zeros(len(self.basis),1))
        v3 = sum([i*j for i,j in zip(v3_vars,self.basis)],zeros(len(self.basis),1))
        print(v1,v2,v3)

class itervar:
    def __init__(self,dict):
        self.dict = dict

    def __call__(self,idx):
        return self.dict[idx]

e1 = Matrix([1,0,0])
e2 = Matrix([0,1,0])
e3 = Matrix([0,0,1])

e = itervar({1:e1,2:e2,3:e3})

H = Matrix([[2,-I,0],[I,1,1],[0,1,2]])

space = VectorSpace([e1,e2,e3])

space.verifybasis()
