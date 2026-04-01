
PC1 = []
PC2 = []

def E(R):
    return None


def Si(X):
    return None


def xor(R,J):
    return None


def split(X,n):
    return None


def IPt(X):
    return None


def concatBinary(x,y):
    return None


def P(R):
    return None


def IP(M):
    return None


def PCX(K, n):
    if n == 1:
        PC = PC1
    elif n == 2:
        PC = PC2
    else:
        raise Exception('Numero errado de matriz PCx')


def leftshift(X, j):
    return None


def KeySchedule(K):
    Kp1 = PCX(K, 1)
    C, D = split(Kp1, 2)
    Ci = [].append(C)
    Di = [].append(D)
    Ki = [].append(Kp1) # precisa disso?
    for i in range(1,16):
        j = 1 if i in (1,2,9,16) else 2
        Ci.append(leftshift(Ci[i-1],j))
        Di.append(leftshift(Di[i-1],j))

        Ki.append(PCX(concatBinary(Ci[i],Di[i]),2))

    return Ki


def f(J,R):
    Rx = E(R)

    RxJ = xor(R,J)

    Ri = split(Rx,8) 
    
    for i in range(1, 8):
        Ri[i] = Si(Ri)

    R = P(concatBinary(Ri))

    return R


def DES(K: bytes, M: bytes, nKeySchedule: int) -> bytes:

    print('Primeiro, roda as 16 iterações do key schedule')
    Ki = []
    Kt = K
    for i in range(1,nKeySchedule):
        Kt = KeySchedule(Kt)
        Ki.append(Kt)

    print('Roda a permutação IP')
    M, L, R = IP(M)

    # M <- L0 || R0

    for i in range(1, 16):
        L[i] = R[i-1]
        R[i] = f(Ki[i],R[i-1])

    C = IPt (concatBinary(L[16],R[16]))

    return C


if __name__ == '__main__':

    DES(
        b'10010010010010010010010010010010010010010010010010010010',
        b'1001001001001001001001001001001001001001001001001001001001001001'
    )
