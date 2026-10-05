import sys
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

from order_necessity_gate import _require_certified_milp_result


def expect_reject(result, gap=1e-10):
    try:
        _require_certified_milp_result(result,gap)
    except RuntimeError:
        return
    raise AssertionError('uncertified MILP result was accepted')


# A feasible incumbent from an interrupted solve must not be reported as optimal.
expect_reject(SimpleNamespace(
    fun=0.25,
    x=[1.0],
    success=False,
    status=1,
    message='time limit reached',
    mip_gap=0.2,
    mip_dual_bound=0.20,
))

# A nominally successful result without the requested gap certificate is also rejected.
expect_reject(SimpleNamespace(
    fun=0.25,
    x=[1.0],
    success=True,
    status=0,
    message='reported success',
    mip_gap=1e-3,
    mip_dual_bound=0.249,
))

# Missing/non-finite certificate fields are rejected.
expect_reject(SimpleNamespace(
    fun=0.25,
    x=[1.0],
    success=True,
    status=0,
    message='reported success',
    mip_gap=None,
    mip_dual_bound=0.25,
))

accepted=_require_certified_milp_result(SimpleNamespace(
    fun=0.25,
    x=[1.0],
    success=True,
    status=0,
    message='optimal',
    mip_gap=0.0,
    mip_dual_bound=0.25,
),1e-10)

assert accepted['success'] is True
assert accepted['status']==0
assert accepted['mip_gap']==0.0
assert accepted['mip_dual_bound']==0.25

print('PASS solver certification guard')
