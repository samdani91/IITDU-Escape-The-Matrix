#!/usr/bin/env python3
import hashlib
P=1000000007
S0=(194723, 837421)
S7=(782941194, 212834238)
S14=(767842069, 154330161)
CIPHERTEXT=bytes.fromhex("2ecf6fb75a2208a7e08c5dc41d97ad6a9d17c7484fa81370b77054f64486ea3a44f1f231")

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))%P for j in range(2)) for i in range(2))
def mv(A,v):
    return tuple(sum(A[i][k]*v[k] for k in range(2))%P for i in range(2))
def mp(A,n):
    R=((1,0),(0,1))
    while n:
        if n&1:R=mm(R,A)
        A=mm(A,A);n//=2
    return R
def inv(A):
    a,b=A[0];c,d=A[1]
    det=(a*d-b*c)%P
    di=pow(det,P-2,P)
    return ((d*di%P,-b*di%P),(-c*di%P,a*di%P))
X=((S0[0],S7[0]),(S0[1],S7[1]))
Y=((S7[0],S14[0]),(S7[1],S14[1]))
A7=mm(Y,inv(X))
final=mv(mp(A7,17),S0)
seed=hashlib.sha256(f"{final[0]}:{final[1]}::THE_LAST_HUNT::rabbit".encode()).digest()
out=bytearray()
for bi in range((len(CIPHERTEXT)+31)//32):
    ks=hashlib.sha256(seed+bi.to_bytes(4,"big")).digest()
    chunk=CIPHERTEXT[bi*32:(bi+1)*32]
    out.extend(a^b for a,b in zip(chunk,ks))
print("A7 =",A7)
print("Final state =",final)
print("Plaintext =",out.decode())
