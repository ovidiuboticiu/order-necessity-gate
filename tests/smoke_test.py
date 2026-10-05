import itertools
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'examples'))

from order_necessity_gate import order_necessity_gap
from core import best_open_loop_ig
from models import ORDER_KEY_v1,DCR,K2,REGIME

key=order_necessity_gap(ORDER_KEY_v1(),time_limit=60,mip_rel_gap=1e-10)
assert abs(key['IG_opt']-1.0)<=1e-9
assert abs(key['IG_best_SA']-.5)<=1e-9
assert abs(key['OrderNecessityGap']-.5)<=1e-9
assert key['solver_certified_optimal'] is True
assert key['mip_gap']<=1e-10

best=None
for r,q,h in itertools.product((.65,.80,.95),(.65,.80,.95),(.10,.25,.40)):
    z=order_necessity_gap(DCR(r,q,h),time_limit=60,mip_rel_gap=1e-10)
    assert z['solver_certified_optimal'] is True
    assert z['mip_gap']<=1e-10
    row=(z['OrderNecessityGap'],r,q,h)
    if best is None or row>best:
        best=row

assert abs(best[0]-0.018933608625138487)<=1e-9
assert best[1:]==(.8,.95,.1)

k2=K2((.85,.70,.60),(.625,.865,.6375),W=5)
k2z=order_necessity_gap(k2,time_limit=60,mip_rel_gap=1e-10)
k2ol,_=best_open_loop_ig(k2)
assert abs((k2z['IG_opt']-k2ol)-0.07371004163477379)<=1e-9
assert abs(k2z['OrderNecessityGap'])<=1e-12

reg=order_necessity_gap(REGIME(.95,.50,.95,.12,5),time_limit=60,mip_rel_gap=1e-10)
assert abs(reg['IG_opt']-0.7713565820675281)<=1e-9
assert abs(reg['OrderNecessityGap'])<=1e-12

print('PASS',{
    'order_key_gap':key['OrderNecessityGap'],
    'dcr_max':best,
    'k2_gap':k2z['OrderNecessityGap'],
    'regime_gap':reg['OrderNecessityGap']
})
