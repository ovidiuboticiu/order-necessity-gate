from __future__ import annotations
import collections
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
from core import Hb, H0, tree, opt_policy

def S_A(acts, obs, n_actions=3, n_obs=2):
    c=[0]*(n_actions*n_obs)
    for a,o in zip(acts,obs):
        c[a*n_obs+o]+=1
    return tuple(c)

def enumerate_environment(M,n_actions=3):
    W=M.W
    hist_w={((),()):M.w0.copy()}
    by_depth={0:[((),())]}
    pred={}
    terminal_entropy={}
    for t in range(W+1):
        if t==W:
            for h in by_depth[t]:
                w=hist_w[h]
                P=float(w.sum())
                p1=float(w[M.tgt].sum()/P) if P>0 else .5
                terminal_entropy[h]=Hb(p1)
            break
        nxt=[]
        for h in by_depth[t]:
            acts,obs=h
            w=hist_w[h]
            P=float(w.sum())
            hist=tuple(zip(acts,obs))
            for a in range(n_actions):
                p1_vec=M.emit(t+1,hist,a)
                p1=float((w*p1_vec).sum()/P) if P>0 else .5
                pred[(h,a)]=p1
                for o in (0,1):
                    h2=(acts+(a,),obs+(o,))
                    hist_w[h2]=w*(p1_vec if o else 1-p1_vec)
                    nxt.append(h2)
        by_depth[t+1]=nxt
    return by_depth,pred,terminal_entropy,hist_w

def bayes_order_aware(M,n_actions=3):
    leaf=tree(M,n_actions)
    pol=opt_policy(leaf,M.W,n_actions)
    return float(H0(M)-pol[((),())][0]),pol

def onpolicy_conflict_certificate(M,n_actions=3):
    ig_opt,pol=bayes_order_aware(M,n_actions)
    d={((),()):M.w0.copy()}
    rows=[]
    total=0
    mass=0.0
    for t in range(M.W):
        groups=collections.defaultdict(list)
        for key,w in d.items():
            groups[S_A(*key,n_actions=n_actions)].append((pol[key][1],float(w.sum())))
        conflicts=[]
        for s,rs in groups.items():
            acts={a for a,_ in rs}
            if len(acts)>1:
                m=sum(p for _,p in rs)
                conflicts.append((s,sorted(acts),m))
                total+=1
                mass+=m
        rows.append({'t':t,'n_classes':len(groups),'conflicts':conflicts})
        nd={}
        for key,w in d.items():
            acts,obs=key
            a=pol[key][1]
            hist=tuple(zip(acts,obs))
            p1=M.emit(t+1,hist,a)
            for o in (0,1):
                nd[(acts+(a,),obs+(o,))]=w*(p1 if o else 1-p1)
        d=nd
    return {
        'IG_opt':ig_opt,
        'conflict_classes':total,
        'conflict_mass':mass,
        'per_t':rows,
        'zero_conflict_certificate':total==0
    }

def _require_certified_milp_result(result, requested_mip_rel_gap):
    if result.fun is None or result.x is None:
        raise RuntimeError(f'MILP returned no usable solution: {result.message}')

    success=bool(result.success)
    status=int(result.status)
    mip_gap=getattr(result,'mip_gap',None)
    dual_bound=getattr(result,'mip_dual_bound',None)

    if not success or status!=0:
        raise RuntimeError(
            'MILP result is not certified optimal: '
            f'success={success}, status={status}, message={result.message}'
        )
    if mip_gap is None or not np.isfinite(float(mip_gap)):
        raise RuntimeError('MILP result lacks a finite mip_gap certificate')
    if float(mip_gap)>float(requested_mip_rel_gap)+1e-12:
        raise RuntimeError(
            'MILP optimality gap exceeds requested tolerance: '
            f'{mip_gap} > {requested_mip_rel_gap}'
        )
    if dual_bound is None or not np.isfinite(float(dual_bound)):
        raise RuntimeError('MILP result lacks a finite dual bound')

    return {
        'success':success,
        'status':status,
        'mip_gap':float(mip_gap),
        'mip_dual_bound':float(dual_bound),
    }


def best_SA_policy_milp(M,n_actions=3,time_limit=120.0,mip_rel_gap=1e-10):
    W=M.W
    by_depth,pred,terminal_entropy,_=enumerate_environment(M,n_actions)
    histories=[h for t in range(W+1) for h in by_depth[t]]
    nonterminal=[h for t in range(W) for h in by_depth[t]]
    q_idx={h:i for i,h in enumerate(histories)}
    off=len(q_idx)
    f_idx={}
    for h in nonterminal:
        for a in range(n_actions):
            f_idx[(h,a)]=off
            off+=1
    states=sorted({S_A(*h,n_actions=n_actions) for h in nonterminal}, key=lambda s:(sum(s),s))
    y_idx={}
    for s in states:
        for a in range(n_actions):
            y_idx[(s,a)]=off
            off+=1
    nvar=off
    c=np.zeros(nvar)
    for h,ent in terminal_entropy.items():
        c[q_idx[h]]=ent
    lb=np.zeros(nvar)
    ub=np.ones(nvar)
    integrality=np.zeros(nvar,dtype=np.int32)
    for i in y_idx.values():
        integrality[i]=1
    rows=[]
    los=[]
    his=[]
    rows.append({q_idx[((),())]:1.0})
    los.append(1.0)
    his.append(1.0)
    for s in states:
        rows.append({y_idx[(s,a)]:1.0 for a in range(n_actions)})
        los.append(1.0)
        his.append(1.0)
    for h in nonterminal:
        q=q_idx[h]
        d={q:-1.0}
        for a in range(n_actions):
            d[f_idx[(h,a)]]=1.0
        rows.append(d)
        los.append(0.0)
        his.append(0.0)
        s=S_A(*h,n_actions=n_actions)
        for a in range(n_actions):
            f=f_idx[(h,a)]
            rows.append({f:1.0,q:-1.0})
            los.append(-np.inf)
            his.append(0.0)
            rows.append({f:1.0,y_idx[(s,a)]:-1.0})
            los.append(-np.inf)
            his.append(0.0)
            p1=pred[(h,a)]
            for o,p in ((0,1-p1),(1,p1)):
                h2=(h[0]+(a,),h[1]+(o,))
                rows.append({q_idx[h2]:1.0,f:-p})
                los.append(0.0)
                his.append(0.0)
    A=lil_matrix((len(rows),nvar),dtype=float)
    for i,d in enumerate(rows):
        for j,v in d.items():
            A[i,j]=v
    result=milp(
        c,
        integrality=integrality,
        bounds=Bounds(lb,ub),
        constraints=LinearConstraint(A.tocsr(),np.asarray(los),np.asarray(his)),
        options={'time_limit':time_limit,'mip_rel_gap':mip_rel_gap,'presolve':True}
    )
    cert=_require_certified_milp_result(result,mip_rel_gap)
    ig_best=float(H0(M)-result.fun)
    chosen={}
    if result.x is not None:
        for s in states:
            vals=[result.x[y_idx[(s,a)]] for a in range(n_actions)]
            chosen[s]=int(np.argmax(vals))
    return {
        'success':cert['success'],
        'status':cert['status'],
        'solver_certified_optimal':True,
        'message':str(result.message),
        'objective_entropy':float(result.fun),
        'mip_dual_bound':cert['mip_dual_bound'],
        'IG_best_SA':ig_best,
        'mip_gap':cert['mip_gap'],
        'mip_node_count':getattr(result,'mip_node_count',None),
        'n_variables':nvar,
        'n_constraints':len(rows),
        'n_binary':len(y_idx),
        'policy':chosen
    }

def order_necessity_gap(M,solve_if_conflict=True,n_actions=3,**milp_kwargs):
    cert=onpolicy_conflict_certificate(M,n_actions=n_actions)
    if cert['zero_conflict_certificate']:
        return {
            **cert,
            'IG_best_SA':cert['IG_opt'],
            'OrderNecessityGap':0.0,
            'method':'zero-conflict exact certificate'
        }
    if not solve_if_conflict:
        return {
            **cert,
            'IG_best_SA':None,
            'OrderNecessityGap':None,
            'method':'conflict detected; MILP not run'
        }
    sol=best_SA_policy_milp(M,n_actions=n_actions,**milp_kwargs)
    return {
        **cert,
        **{k:v for k,v in sol.items() if k!='policy'},
        'OrderNecessityGap':cert['IG_opt']-sol['IG_best_SA'],
        'policy':sol['policy'],
        'method':'global MILP with certified optimum after conflict'
    }
