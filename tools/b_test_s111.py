"""S111 item (b) - the pre-registered offline test (S111_B_PREREG.md). Parts A-E and G.
Kept as the record of the test docs/S111_B_PREREG.md fixed before its data (results: docs/S111_B_RESULTS.md).
Needs numpy, pandas, scipy, statsmodels and xlrd; not run in CI.
usage: python tools/b_test_s111.py <outcomes.csv> [<reports.csv> <gpr_daily.xls>]
       python tools/b_test_s111.py --full <export7b.csv> <outdir> <gpr_daily.xls>"""
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


def dm_hln(d, h=2):
    """One-sided DM test that mean(d) > 0, as statsmodels implements it:
    diebold_mariano_test(lags=h-1, harvey_adj=True, horizon=h), HAC long-run variance,
    HLN correction, Student t(T-1). d is passed as a loss differential (forecast A = climatology)."""
    from statsmodels.tsa.stattools import diebold_mariano_test
    d = np.asarray(d, float)
    T = len(d)
    c = 1.0 + max(0.0, -d.min())
    y = np.zeros(T)
    r = diebold_mariano_test(y, np.sqrt(d + c), np.full(T, np.sqrt(c)), lags=h - 1, harvey_adj=True, horizon=h)
    return d.mean(), float(r.statistic), float(stats.t.sf(r.statistic, T - 1)), T


def part_ae(path):
    o = pd.read_csv(path)
    o = o.dropna(subset=['spy_change_7d', 'sentiment_score']).copy()
    o['created_at'] = pd.to_datetime(o['created_at'], utc=True, format='mixed')
    iso = o['created_at'].dt.isocalendar()
    o['week'] = iso['year'].astype(str) + '-W' + iso['week'].astype(str).str.zfill(2)
    o['x'] = -o['sentiment_score'].astype(float)
    o['y'] = (o['spy_change_7d'].astype(float) <= -1.0).astype(int)
    print('rows %d, weeks %d, events %d (base rate %.3f)' % (len(o), o['week'].nunique(), o['y'].sum(), o['y'].mean()))
    fm, fc = np.full(len(o), np.nan), np.full(len(o), np.nan)
    for w in o['week'].unique():
        te = (o['week'] == w).values
        tr = ~te
        X = sm.add_constant(o.loc[tr, 'x'].values)
        try:
            m = sm.Logit(o.loc[tr, 'y'].values, X).fit(disp=0)
            fm[te] = m.predict(sm.add_constant(o.loc[te, 'x'].values, has_constant='add'))
        except Exception as e:
            print('fold', w, 'logit failed:', e)
            fm[te] = o.loc[tr, 'y'].mean()
        fc[te] = o.loc[tr, 'y'].mean()
    o['f_model'], o['f_clim'] = fm, fc
    bs_m = np.mean((o['f_model'] - o['y']) ** 2)
    bs_c = np.mean((o['f_clim'] - o['y']) ** 2)
    print('Brier model %.4f, climatology %.4f, BSS %.4f' % (bs_m, bs_c, 1 - bs_m / bs_c))
    o['d'] = (o['f_clim'] - o['y']) ** 2 - (o['f_model'] - o['y']) ** 2
    wk = o.groupby('week')['d'].mean().sort_index()
    dbar, hln, p, T = dm_hln(wk.values, h=2)
    print('DM/HLN on %d weekly means: mean d %.5f, stat %.3f, one-sided p %.4f' % (T, dbar, hln, p))
    o['bin'] = pd.qcut(o['f_model'], 5, duplicates='drop')
    rel = o.groupby('bin', observed=True).agg(n=('y', 'size'), mean_forecast=('f_model', 'mean'), observed=('y', 'mean'))
    print('reliability (out-of-fold):'); print(rel.round(3).to_string())
    full = sm.Logit(o['y'].values, sm.add_constant(o['x'].values)).fit(disp=0)
    print('full-data fit (frozen for part F if A-E pass): a=%.4f b=%.4f' % tuple(full.params))
    ok = (1 - bs_m / bs_c) > 0 and p < 0.05
    print('PASS A-E' if ok else 'FAIL A-E', '(BSS > 0 and p < 0.05 required)')


def part_g(rep_path, gpr_path):
    r = pd.read_csv(rep_path)
    r['created_at'] = pd.to_datetime(r['created_at'], utc=True, format='mixed')
    r = r.dropna(subset=['escalation_score_raw'])
    r['day'] = r['created_at'].dt.tz_convert(None).dt.normalize()
    g = pd.read_excel(gpr_path)
    print('GPR columns:', list(g.columns)[:12])
    # 'date' is a real date; 'DAY' is an int like 20261002
    g['day'] = pd.to_datetime(g['date']).dt.normalize()
    daily = r.groupby('day')['escalation_score_raw'].mean().rename('esc')
    m = g.set_index('day').join(daily, how='inner')
    iso = m.index.isocalendar()
    m['week'] = iso['year'].astype(str) + '-W' + iso['week'].astype(str).str.zfill(2)
    for col in [c for c in ('GPRD', 'GPRD_THREAT', 'GPRD_ACT') if c in m.columns]:
        wk = m.groupby('week')[[col, 'esc']].mean().sort_index()
        rho, p2 = stats.spearmanr(wk[col], wk['esc'])
        p1 = p2 / 2 if rho > 0 else 1 - p2 / 2
        lag = wk[col].shift(1)
        ok = lag.notna()
        rl, pl2 = stats.spearmanr(lag[ok], wk['esc'][ok])
        pl1 = pl2 / 2 if rl > 0 else 1 - pl2 / 2
        print('%-12s weeks %d  rho %.3f p1 %.4f | GPR lagged 1w: rho %.3f p1 %.4f' % (col, len(wk), rho, p1, rl, pl1))


OUT_COLS = ['report_id', 'created_at', 'sentiment', 'sentiment_score', 'escalation_score',
            'escalation_score_raw', 'risk_level', 'spy_change_3d', 'spy_change_7d', 'spy_change_30d',
            'black_swan_flag']
REP_COLS = ['id', 'created_at', 'escalation_score', 'escalation_score_raw', 'sentiment_score', 'risk_level']


def split_full(path, outdir):
    """S111_EXPORT7b.sql: one row, each *_csv column a whole headerless CSV file."""
    import io, os
    f = pd.read_csv(path)
    o = pd.read_csv(io.StringIO(f['outcomes_csv'][0]), header=None, names=OUT_COLS, na_values=[''])
    r = pd.read_csv(io.StringIO(f['reports_csv'][0]), header=None, names=REP_COLS, na_values=[''])
    print('export says %d outcomes / %d reports; parsed %d / %d'
          % (f['outcome_rows'][0], f['report_rows'][0], len(o), len(r)))
    assert len(o) == f['outcome_rows'][0] and len(r) == f['report_rows'][0], 'row count mismatch'
    po, pr = os.path.join(outdir, 'outcomes_full.csv'), os.path.join(outdir, 'reports_full.csv')
    o.to_csv(po, index=False); r.to_csv(pr, index=False)
    return po, pr


if __name__ == '__main__':
    if sys.argv[1] == '--full':
        po, pr = split_full(sys.argv[2], sys.argv[3])
        part_ae(po)
        part_g(pr, sys.argv[4])
    else:
        part_ae(sys.argv[1])
        if len(sys.argv) > 3:
            part_g(sys.argv[2], sys.argv[3])
