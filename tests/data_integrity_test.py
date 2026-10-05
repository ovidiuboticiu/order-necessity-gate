import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# K2 table must have the exact public schema on every row.
k2_path = ROOT / 'data' / 'k2_results.csv'
with k2_path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

expected_fields = [
    'template', 'rho', 'q1_eff', 'IG_opt', 'IG_best_open_loop', 'AdaptiveGap',
    'onpolicy_action_conflicts', 'onpolicy_state_conflicts', 'OrderNecessityGap',
    'zero_conflict_certificate', 'best_open_loop',
]
assert reader.fieldnames == expected_fields, reader.fieldnames
assert len(rows) == 15, len(rows)
for i, row in enumerate(rows, start=2):
    assert None not in row.values(), f'missing CSV field on line {i}: {row}'

# The public REGIME evidence behind the 26/26 statement must be complete.
regime_path = ROOT / 'data' / 'regime_high_proxy_26.json'
regime = json.loads(regime_path.read_text(encoding='utf-8'))
assert len(regime) == 26, len(regime)
assert all(float(row['G_ord']) >= 0.10 for row in regime)
assert max(abs(float(row['loss_vs_opt'])) for row in regime) <= 1e-12

print('PASS', {
    'k2_rows': len(rows),
    'regime_high_proxy_rows': len(regime),
    'regime_max_abs_loss_vs_opt': max(abs(float(row['loss_vs_opt'])) for row in regime),
})
