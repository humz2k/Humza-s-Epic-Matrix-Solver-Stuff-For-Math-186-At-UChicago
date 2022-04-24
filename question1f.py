import numpy as np

def dagger(v1):
    return v1.conj().T

def v(x):
    if x == 1:
        return np.array([[0.+1.j],[-2.+0.j],[1.+0.j]])
    if x == 2:
        return np.array([[0.-1.j],[0.+0.j],[1.+0.j]])
    if x == 3:
        return np.array([[0.+1.j],[1.+0.j],[1.+0.j]])

#print(np.matmul(v1,v1.conj().T))

print(np.matmul(v(1),dagger(v(1))))
