"""
PR-1 .. PR-5. Runs strictly the tests registered in PREREGISTRATION.md (commit 2ce9bc1).
No test is added, dropped or re-specified here.
"""
import numpy as np, pandas as pd, json
from scipy import stats, integrate

RNG = np.random.default_rng(20260828)
OUT = {}
def head(s): print("\n"+"="*78+f"\n{s}\n"+"="*78)

# ---------------------------------------------------------------- predictions
SQ6 = np.pi/np.sqrt(6)
MODELS = {"A  CV=1.28255*Om^2 (A.12 mode-on-wall)": lambda O: SQ6*O**2,
          "A' CV=1.28255*Om   (A.12, multiplier 1)": lambda O: SQ6*O,
          "B  CV=Om/2        (Sec 2.3 quantal)":     lambda O: O/2}
OM = {"Z2": 1/np.pi, "SO(2)": 1/(2*np.pi), "Z3": 1/(3*np.pi)}

# ---------------------------------------------------------------- D1
df = pd.read_csv('/home/user/CRR/crr-cv-predictions/data/cv_predictions_132.csv')
mine = pd.read_csv('/home/user/CRR/crr_v012_validation/data/systems132.csv')
head("Cross-check: independent parse of 132.pdf Table 8 vs repo CSV")
m = mine.merge(df[['system','class','symmetry','cv_obs']], on='system', how='inner', suffixes=('_p',''))
agree_cv  = np.isclose(m.cv_obs_p, m.cv_obs, rtol=1e-6, atol=1e-9).mean()
agree_cls = (m.cls == m['class']).mean(); agree_sym = (m.sym == m.symmetry).mean()
print(f"  matched {len(m)}/132 by name; CV agree {agree_cv:.1%}, class agree {agree_cls:.1%}, symmetry agree {agree_sym:.1%}")
OUT['parse_crosscheck'] = dict(n=len(m), cv=float(agree_cv), cls=float(agree_cls), sym=float(agree_sym))

df['Omega'] = df.symmetry.map(OM)
A = df[(df['class']=='A') & df.symmetry.isin(['Z2','SO(2)'])].copy()
print(f"\nClass A, symmetry in {{Z2,SO(2)}}: n = {len(A)}  "
      f"(Z2 {sum(A.symmetry=='Z2')}, SO(2) {sum(A.symmetry=='SO(2)')})")

def boot_median(x, B=100000):
    x=np.asarray(x); s=RNG.choice(x,(B,len(x)),replace=True)
    return np.percentile(np.median(s,axis=1),[2.5,97.5])
def boot_ratio(a,b,B=100000):
    a=np.asarray(a); b=np.asarray(b)
    r=np.median(RNG.choice(a,(B,len(a)),replace=True),axis=1)/np.median(RNG.choice(b,(B,len(b)),replace=True),axis=1)
    return np.median(r), np.percentile(r,[2.5,97.5])

# --------------------------------------------------------------- PR-1.1 ratio
head("PR-1.1  class ratio  median CV(Z2,A) / median CV(SO(2),A)")
z = A[A.symmetry=='Z2'].cv_obs.values; s = A[A.symmetry=='SO(2)'].cv_obs.values
r, ci = boot_ratio(z,s)
print(f"  observed ratio = {r:.3f}   95% CI [{ci[0]:.3f}, {ci[1]:.3f}]   (n_Z2={len(z)}, n_SO2={len(s)})")
for nm,pred in [("A", 4.00), ("A'", 2.00), ("B", 2.00)]:
    verdict = "SURVIVES" if ci[0] <= pred <= ci[1] else "REJECTED"
    print(f"    {nm:3s} predicts {pred:.2f}  ->  {verdict}")
OUT['PR1_1'] = dict(ratio=float(r), ci=[float(ci[0]),float(ci[1])],
                    A='SURVIVES' if ci[0]<=4<=ci[1] else 'REJECTED',
                    AB='SURVIVES' if ci[0]<=2<=ci[1] else 'REJECTED')

# --------------------------------------------------------------- PR-1.2 abs
head("PR-1.2  absolute location of each cell median")
rows=[]
for sym in ['Z2','SO(2)']:
    x = A[A.symmetry==sym].cv_obs.values; med=np.median(x); ci2=boot_median(x)
    print(f"\n  {sym:6s} n={len(x):2d}  median CV = {med:.4f}  95% CI [{ci2[0]:.4f}, {ci2[1]:.4f}]")
    for nm,f in MODELS.items():
        p=f(OM[sym]); v = "SURVIVES" if ci2[0]<=p<=ci2[1] else "REJECTED"
        print(f"      {nm:42s} predicts {p:.5f}  ->  {v}   (obs/pred = {med/p:.2f})")
        rows.append(dict(sym=sym,model=nm,pred=float(p),median=float(med),
                         ci=[float(ci2[0]),float(ci2[1])],verdict=v,ratio=float(med/p)))
OUT['PR1_2']=rows

# --------------------------------------------------------------- PR-1.3 AIC
head("PR-1.3  zero-parameter model comparison (lognormal residual, 1 nuisance scale each)")
y = np.log(A.cv_obs.values); Om = A.Omega.values
res={}
for nm,f in MODELS.items():
    mu = np.log(f(Om)); e = y-mu
    sig = np.sqrt(np.mean(e**2))                    # MLE of the one nuisance parameter
    ll = -len(y)/2*np.log(2*np.pi*sig**2) - np.sum(e**2)/(2*sig**2)
    aic = 2*1 - 2*ll
    res[nm]=dict(loglik=float(ll),aic=float(aic),sigma=float(sig),bias=float(np.mean(e)))
best=min(res,key=lambda k:res[k]['aic'])
for nm,v in sorted(res.items(),key=lambda kv:kv[1]['aic']):
    print(f"  {nm:42s} AIC {v['aic']:8.2f}  dAIC {v['aic']-res[best]['aic']:7.2f}  "
          f"sigma_log {v['sigma']:.3f}  mean log-bias {v['bias']:+.3f}")
print(f"\n  best = {best}; dAIC>10 is decisive against a model.")
OUT['PR1_3']=res; OUT['PR1_3_best']=best

# --------------------------------------------------------------- PR-1.4 slope
head("PR-1.4  scaling exponent: regress log CV on log Omega (Class A)")
sl, ic, rv, pv, se = stats.linregress(np.log(Om), y)
lo,hi = sl-1.96*se, sl+1.96*se
print(f"  slope = {sl:.3f}  95% CI [{lo:.3f}, {hi:.3f}]   r={rv:.3f}  p={pv:.2e}")
for nm,e in [("A",2.0),("A'",1.0),("B",1.0)]:
    print(f"    {nm:3s} predicts exponent {e:.1f}  ->  {'SURVIVES' if lo<=e<=hi else 'REJECTED'}")
OUT['PR1_4']=dict(slope=float(sl),ci=[float(lo),float(hi)],p=float(pv),r=float(rv))

# --------------------------------------------------------------- D2 EEG replication
head("PR-1 replication on D2 (PhysioNet EEGBCI PLV-CV, N=109) and D3 (MPI-LEMON, N=189)")
D2 = pd.DataFrame([  # 132.pdf Table 2
 ("Delta","Z2","A",0.152),("Theta","Z2","B",0.127),("Alpha","Z2","A",0.153),
 ("Beta-2","SO(2)","A",0.105),("Gamma","SO(2)","A",0.066)],
 columns=["band","sym","cls","cv"])
D3 = pd.DataFrame([  # 132.pdf Table 3, EC
 ("Delta","Z2","A",0.200,0.256,+0.46,0.012),("Theta","Z2","B",0.204,0.216,+0.18,0.272),
 ("Alpha","Z2","C",0.262,0.281,+0.20,0.217),("Beta","Z2","A",0.163,0.160,-0.06,0.693),
 ("LowGamma","SO(2)","A",0.113,0.117,+0.14,0.388)],
 columns=["band","sym","cls","young","old","d","p"])
for label,sub in [("D2 PLV (Class A bands)", D2[D2.cls=='A']),
                  ("D3 envelope, young (Class A bands)", D3[D3.cls=='A'].assign(cv=lambda t:t.young)),
                  ("D3 envelope, old   (Class A bands)", D3[D3.cls=='A'].assign(cv=lambda t:t.old))]:
    zz=sub[sub.sym=='Z2'].cv.values; ss=sub[sub.sym=='SO(2)'].cv.values
    print(f"\n  {label}: Z2 mean {zz.mean():.4f} (n={len(zz)}), SO(2) mean {ss.mean():.4f} (n={len(ss)}), "
          f"ratio {zz.mean()/ss.mean():.2f}")
    for nm,f in MODELS.items():
        pz,ps=f(OM['Z2']),f(OM['SO(2)'])
        print(f"      {nm:42s} Z2 obs/pred {zz.mean()/pz:5.2f}   SO(2) obs/pred {ss.mean()/ps:5.2f}")

# --------------------------------------------------------------- PR-2 skew
head("PR-2  interval skew")
E = RNG.exponential(size=4000000); T = np.log(1/1e-9) + np.log(E)
print(f"  Route A/A' predict skew(T) = skew(log Exp(1)) = {stats.skew(T):+.4f}  (exact: -1.13955)")
print("""  Standard published morphology of the D1 cyclic interval distributions
  (neuronal ISI, cardiac RR, Ca2+ spike intervals, somite-clock periods) is a
  unimodal distribution with a LONG RIGHT TAIL -- gamma / lognormal / inverse-
  Gaussian family, POSITIVE skew. No CRR variant predicts positive skew.
    -> Routes A and A' REJECTED as accounts of CYCLIC rupture.
  Human age-at-death, by contrast, is strongly NEGATIVELY skewed and is the
  canonical Gompertz application.
    -> Route A SUPPORTED for TERMINAL rupture.
  Registered interpretation: A.12 is a senescence law that Sec 2.3 misapplies to
  stationary cycling.""")
OUT['PR2']=dict(predicted_skew=float(stats.skew(T)))

# --------------------------------------------------------------- PR-3 development
head("PR-3  developmental Omega schedule (D3, MPI-LEMON young vs old, 5 bands)")
print("  v01.2 requires Omega non-increasing with age -> every band's d must be <= 0")
for _,r in D3.iterrows():
    print(f"    {r.band:9s} {r.sym:6s} young {r.young:.3f} -> old {r.old:.3f}   d = {r.d:+.2f}  p={r.p:.3f}"
          f"   [{'as predicted' if r.d<=0 else 'AGAINST prediction'}]")
neg=(D3.d<=0).sum(); pos=(D3.d>0).sum()
sign_p = stats.binomtest(int(neg), 5, 0.5, alternative='greater').pvalue
print(f"\n  {neg}/5 in the predicted direction, {pos}/5 against.  sign test p = {sign_p:.3f}")
print(f"  Decision rule required >=4/5 negative.  ->  PREDICTION {'PASSES' if neg>=4 else 'FAILS'}")
print(f"  Inverting the surviving law CV=Om/2: implied Omega young {2*D3.young.mean():.3f} -> old {2*D3.old.mean():.3f}"
      f"  (Omega RISES by {100*(D3.old.mean()/D3.young.mean()-1):.1f}%)")
OUT['PR3']=dict(neg=int(neg),pos=int(pos),sign_p=float(sign_p),verdict='FAILS' if neg<4 else 'PASSES',
                omega_young=float(2*D3.young.mean()),omega_old=float(2*D3.old.mean()))

# --------------------------------------------------------------- PR-4 precision
head("PR-4  precision lowers Omega (D4, eyes-closed -> eyes-open)  [non-independent]")
D4 = pd.DataFrame([("Delta","Z2",0.220,0.180,0.54,0.083),("Theta","Z2",0.219,0.190,0.39,0.041),
                   ("Alpha","Z2",0.266,0.236,0.53,0.012),("Beta","Z2",0.162,0.135,0.65,0.001),
                   ("LowGamma","SO(2)",0.121,0.120,0.005,0.983)],
                  columns=["band","sym","EC","EO","d","p"])
for _,r in D4.iterrows():
    print(f"    {r.band:9s} {r.sym:6s} EC {r.EC:.3f} -> EO {r.EO:.3f}   d={r.d:.3f}  p={r.p:.3f}")
z4=D4[D4.sym=='Z2']; g4=D4[D4.sym=='SO(2)']
ok = (z4.d>0).all() and g4.d.iloc[0] < z4.d.min()
print(f"\n  4/4 Z2 bands decrease: {(z4.d>0).all()};  SO(2) effect {g4.d.iloc[0]:.3f} < min Z2 effect {z4.d.min():.3f}: "
      f"{g4.d.iloc[0]<z4.d.min()}")
print(f"  -> {'CONSISTENT' if ok else 'INCONSISTENT'} (scored as consistency only; capped at T2, cf. PREREGISTRATION 5)")
OUT['PR4']=dict(consistent=bool(ok))

# --------------------------------------------------------------- PR-5 holding
head("PR-5  holding raises effective Omega  [EXPLORATORY]")
dy = ['Conversation turn-taking gap','Neonatal inter-cry interval','Infant suckling burst']
sub = df[df.system.isin(dy)][['system','class','symmetry','cv_obs']]
solo, held = 0.5/np.pi, (0.5/np.pi)*np.sqrt(2)
print(f"  solitary Z2 baseline CV = {solo:.5f}   held (f=1/2) prediction = {held:.5f}")
wins=0
for _,r in sub.iterrows():
    ls, lh = abs(np.log(r.cv_obs/solo)), abs(np.log(r.cv_obs/held))
    better = 'HELD' if lh<ls else 'SOLITARY'
    wins += (lh<ls)
    f_imp = 1 - (solo/r.cv_obs)**2
    print(f"    {r.system:32s} ({r['class']},{r.symmetry}) CV={r.cv_obs:.3f}  "
          f"|log ratio| solo {ls:.3f} vs held {lh:.3f} -> {better};  implied f = {f_imp:+.2f}")
print(f"\n  held prediction closer for {wins}/{len(sub)} dyadic systems -> "
      f"{'FAVOURS the holding correction' if wins>len(sub)/2 else 'does not favour it'}")
print("  [EXPLORATORY: analyst had seen these rows. T1 only. Re-registered as F1/F2.]")
OUT['PR5']=dict(n=int(len(sub)),wins=int(wins))

json.dump(OUT, open('/home/user/CRR/crr_v012_validation/results/prereg_results.json','w'), indent=1, default=str)
print("\nwrote results/prereg_results.json")
