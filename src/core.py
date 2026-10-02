import itertools
import numpy as np

LOG2=np.log2

def Hb(p):
    p=min(max(float(p),0.0),1.0)
    return 0.0 if p<=0 or p>=1 else float(-(p*LOG2(p)+(1-p)*LOG2(1-p)))

class Model:
    """Finite-horizon binary-observation model.

    paths: latent rows; w0: prior weights; tgt: bool mask target==1;
    emit(t, hist, a) -> vector P(o=1) for each latent row.
    """
    def __init__(self, paths, w0, tgt, emit, W):
        self.paths=np.asarray(paths)
        self.w0=np.asarray(w0,dtype=float)
        self.tgt=np.asarray(tgt,dtype=bool)
        self.emit=emit
        self.W=W

def tree(M, n_actions=3):
    leaf={}
    def rec(acts,obs,w):
        t=len(acts)
        if t==M.W:
            P=w.sum()
            leaf[(acts,obs)]=0.0 if P<=0 else P*Hb(w[M.tgt].sum()/P)
            return
        hist=tuple(zip(acts,obs))
        for a in range(n_actions):
            p1=M.emit(t+1,hist,a)
            rec(acts+(a,),obs+(1,),w*p1)
            rec(acts+(a,),obs+(0,),w*(1-p1))
    rec((),(),M.w0.copy())
    return leaf

def opt_policy(leaf,W,n_actions=3):
    memo={}
    def V(acts,obs):
        t=len(acts)
        if t==W:
            return leaf[(acts,obs)]
        k=(acts,obs)
        if k in memo:
            return memo[k][0]
        vals=[V(acts+(a,),obs+(0,))+V(acts+(a,),obs+(1,)) for a in range(n_actions)]
        m=min(vals)
        a=vals.index(m)
        memo[k]=(m,a,tuple(vals))
        return m
    V((),())
    return memo

def H0(M):
    return Hb(M.w0[M.tgt].sum()/M.w0.sum())

def best_open_loop_ig(M,n_actions=3):
    leaf=tree(M,n_actions)
    hz=H0(M)
    best=-1.0
    best_seq=None
    for seq in itertools.product(range(n_actions),repeat=M.W):
        ent=sum(leaf[(seq,obs)] for obs in itertools.product((0,1),repeat=M.W))
        ig=hz-ent
        if ig>best:
            best=ig
            best_seq=seq
    return float(best),best_seq
