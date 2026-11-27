# A second jigsaw (illustration, our own simulation). Twenty-four places, laid in a random order. Each piece laid takes one of two colours:
# with probability 0.85 the colour most of its already-laid neighbours have (a coin if they are split or absent), otherwise the other.
# First-order control: the lid is printed first, so every run ends the same.
import numpy as np, json
NX,NY,R=6,4,1000; rng=np.random.default_rng(3)
def run(r):
    g=-np.ones((NY,NX),int); order=r.permutation(NX*NY); seq=[]
    for k in order:
        j,i=divmod(int(k),NX); nb=[g[b,a] for a,b in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)) if 0<=a<NX and 0<=b<NY and g[b,a]>=0]
        maj=int(r.integers(2)) if (not nb or sum(nb)*2==len(nb)) else int(sum(nb)*2>len(nb)); c=maj if r.random()<.85 else 1-maj; g[j,i]=c; seq.append((int(k),c))
    return g,seq
finals=[]; shares=[]; keep=[]
for n in range(R):
    g,seq=run(rng); finals.append(''.join(map(str,g.ravel()))); shares.append(float(g.mean()))
    if n<48: keep.append({'grid':g.ravel().tolist(),'seq':seq})
hist=np.histogram(shares,bins=8,range=(0,1))[0].tolist()
out={'runs':R,'distinct':len(set(finals)),'most_common':max(finals.count(f) for f in set(finals)),'hist':hist,'keep':keep,'first_order_distinct':1}
json.dump(out,open('maths2.json','w')); print(out['distinct'],out['most_common'],hist)
