import numpy as np
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))

from core import Model

def ORDER_KEY_v1():
    rows=[]
    w=[]
    for z in (0,1):
        for c in ((0,1),(1,0)):
            rows.append((z,c[0],c[1]))
            w.append(.25)
    P=np.array(rows,dtype=int)

    def emit(t,hist,a):
        dead=any(aa in (1,2) for aa,_ in hist)
        if dead:
            return np.full(len(P),.5)
        if t in (1,2):
            if a==0:
                return P[:,t].astype(float)
            return np.full(len(P),.5)
        if a==0:
            return np.full(len(P),.5)
        z=P[:,0]
        c0=P[:,1]
        c1=P[:,2]
        good=((c0==0)&(c1==1)) if a==1 else ((c0==1)&(c1==0))
        return np.where(good,z.astype(float),.5)

    return Model(P,w,P[:,0]==1,emit,3)

def DCR(r,q_hi,h,q_lo=.5):
    rows=[]
    ws=[]
    for z in (0,1):
        for m1 in (0,1):
            for m2 in (0,1):
                rows.append((z,m1,m2))
                ws.append(.25*(h if m2!=m1 else 1-h))
    P=np.asarray(rows,dtype=int)
    w=np.asarray(ws,dtype=float)

    def emit(t,hist,a):
        z=P[:,0]
        m1=P[:,1]
        m2=P[:,2]
        if t==1:
            return np.where(m1==1,r,1-r).astype(float) if a==0 else np.full(len(P),.5)
        if t==2:
            return np.where(m2==1,r,1-r).astype(float) if a==0 else np.full(len(P),.5)
        if t==3:
            if a==0:
                return np.full(len(P),.5)
            acc=np.where(m2==(0 if a==1 else 1),q_hi,q_lo)
            return np.where(z==1,acc,1-acc).astype(float)
        raise ValueError(t)

    return Model(P,w,P[:,0]==1,emit,3)

def K2(q0,q1,W=5):
    q0=np.asarray(q0,dtype=float)
    q1=np.asarray(q1,dtype=float)

    def emit(t,hist,a):
        s=0
        for aa,oo in hist:
            if (aa,oo)==(0,1):
                s=1
            elif (aa,oo)==(1,1):
                s=0
        q=q0[a] if s==0 else q1[a]
        return np.array([1-q,q],dtype=float)

    return Model(np.array([[0],[1]]),[.5,.5],[False,True],emit,W)

def REGIME(hi,lo,r,h,W=5):
    import itertools
    rows=[]
    ws=[]
    for z in (0,1):
        for ms in itertools.product((0,1),repeat=W+1):
            wt=.25
            for j in range(1,W+1):
                wt*=h if ms[j]!=ms[j-1] else 1-h
            rows.append((z,)+ms)
            ws.append(wt)
    P=np.array(rows,dtype=int)
    w=np.array(ws,dtype=float)
    cache={}

    def emit(t,hist,a):
        k=(t,a)
        if k not in cache:
            z=P[:,0]
            m=P[:,1+t]
            if a==2:
                p=np.where(m==1,r,1-r)
            else:
                acc=np.where(m==a,hi,lo)
                p=np.where(z==1,acc,1-acc)
            cache[k]=p
        return cache[k]

    return Model(P,w,P[:,0]==1,emit,W)
