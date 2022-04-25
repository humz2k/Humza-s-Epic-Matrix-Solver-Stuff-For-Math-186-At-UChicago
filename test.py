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

#h.print_vals()

print(str_complex(det(H)))
print(eigenvectors(H))
