from matrix import *

e1 = matrix([[1],[0],[0]])
e2 = matrix([[0],[1],[0]])
e3 = matrix([[0],[0],[1]])

H = matrix([[2,-i,0],[i,1,1],[0,1,2]])

e = miter(var.e,{1:e1,2:e2,3:e3})

h = constant(var.h,vars=[var.i,var.j])

expr1 = expr(e(var.i) * (e(var.j)^t)) * h

sig1 = sig({var.i:(1,3),var.j:(1,3)},expr1)

h = sig1.solve(H)

eigenvalues,eigenvectors = eig(H)

v1 = eigenvectors[eigenvalues[0]][0]
v2 = eigenvectors[eigenvalues[1]][0]
v3 = eigenvectors[eigenvalues[2]][0]

v = miter(var.v,{1:v1,2:v2,3:v3})

k = constant(var.k,vars=[var.i,var.j])

raw = expr(v(var.i) * (v(var.j)^t))

expr2 = raw * k

sig2 = sig({var.i:(1,3),var.j:(1,3)},expr2)

k = sig2.solve(H)

print(sig2.solve())
print(H)
