import numpy as np
import scipy.linalg as sla

import time


def Choleski_numpy(A, b):
    ret = {}

    # start timer
    start = time.time()
    # solve
    ret['result'] = np.linalg.solve(A, b)
    # end timer
    end = time.time()
    ret['time'] = end - start
    return ret



def Choleski_sla(A, b):
    ret = {}

    # start timer
    start = time.time()
    # solve
    ret['result'] = sla.solve(A, b)
    # end timer
    end = time.time()
    ret['time'] = end - start
    return ret



def main():
    dim = 3

    A = np.diag(np.array([3.] * dim))
    for i, j in zip(range(1, dim), range(0, dim-1)):
        A[i, j] = -1
        A[j, i] = -1
    
    b = np.array([1.] * dim)
    
    print(f'A: {A}')
    print(f'b: {b}')

    sla_sol = Choleski_sla(A, b)
    np_sol = Choleski_numpy(A, b)

    print(f'Scipy solution {sla_sol}')
    print()
    print(f'NumPy solution {np_sol}')



if __name__ == '__main__':
    main()