#!/usr/bin/env python3
"""Local integrity and entry-level adjudication. External proof authenticity is separate."""
import argparse,datetime,hashlib,json,math,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
META={'FREEZE.json','HASHES.sha256'}
ZERO='0'*64
class GateError(ValueError):pass
def require(test,message):
 if not test:raise GateError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def dump(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()+b'\n'
def read(p):return json.loads(pathlib.Path(p).read_bytes())
def finite(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def stamp(s):
 d=datetime.datetime.fromisoformat(s.replace('Z','+00:00'));require(d.tzinfo is not None,'UTC offset required');return d

def fileset(d):
 d=pathlib.Path(d).resolve();out={}
 for p in sorted(d.rglob('*')):
  require(not p.is_symlink(),'symlink forbidden: '+str(p))
  if p.is_file():
   rel=p.relative_to(d).as_posix()
   if rel in META:continue
   require(p.name not in META,'nested reserved freeze metadata forbidden')
   out[rel]=digest(p.read_bytes())
 return out

def control_metrics(p,outcomes):
 """Use the SAME frozen scoring rule on every numeric witness."""
 for c in outcomes:
  require(set(c)=={'id','expected','units'},'bad control row')
  require(c['expected'] in ['PASS','FAIL'],'bad control expectation')
  got=decision(p,c['units'])['threshold_met']
  require(got==(c['expected']=='PASS'),'control violated: '+c['id'])
 require(any(c['expected']=='PASS' for c in outcomes),'must-pass control absent')
 require(any(c['expected']=='FAIL' for c in outcomes),'must-fail control absent')
 require(len({c['id'] for c in outcomes})==len(outcomes),'duplicate controls')

def protocol(d):
 p=read(pathlib.Path(d)/'PREREG.json')
 required={'study_id','status','layer','hypothesis','bridge','independent_unit','primary','baselines','margin','min_fraction','min_units','metric_bounds','alpha','max_sensitivity_flips','exclusions','multiplicity','data_ids','seen_ids_before_freeze','environment','scorer','prior_art','controls_file','registered_seed_aggregation','same_day_reuse_policy','power_analysis','admissibility_report'}
 require(required<=set(p),'missing protocol fields: '+str(sorted(required-set(p))))
 require(p['status']=='READY_FOR_FIRE','template is NOT REGISTERED / not ready')
 require(p['layer'] in ['engineering','empirical','heuristic'],'unsupported claim layer for generic empirical engine')
 require(len(p['baselines'])>=3 and len(set(p['baselines']))==len(p['baselines']),'strong simple, native and ablation baselines required')
 require(p['primary']=='bounded_paired_margin','generic scorer only supports bounded_paired_margin')
 require(finite(p['margin']) and p['margin']>0,'positive discriminating margin required')
 require(finite(p['min_fraction']) and 0<p['min_fraction']<=1,'bad fraction')
 require(isinstance(p['min_units'],int) and p['min_units']>=2,'bad independent sample count')
 require(len(p['metric_bounds'])==2 and all(finite(x) for x in p['metric_bounds']) and p['metric_bounds'][0]<p['metric_bounds'][1],'bad metric bounds')
 require(finite(p['alpha']) and 0<p['alpha']<1,'bad alpha')
 require(isinstance(p['max_sensitivity_flips'],int) and p['max_sensitivity_flips']>=0,'bad sensitivity limit')
 require(p['data_ids'] and len(set(p['data_ids']))==len(p['data_ids']),'missing/duplicate target IDs')
 require(not set(p['data_ids'])&set(p['seen_ids_before_freeze']),'SEEN data cannot be held out')
 for key in ['hypothesis','bridge','independent_unit','exclusions','multiplicity','registered_seed_aggregation','same_day_reuse_policy']:
  require(isinstance(p[key],str) and p[key].strip() and 'TODO' not in p[key] and 'NOT_REGISTERED' not in p[key],key+' unresolved')
 for key in ['environment','scorer','prior_art','controls_file','power_analysis','admissibility_report']:
  rel=pathlib.Path(p[key]);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe protocol path')
  f=pathlib.Path(d)/rel;require(f.is_file() and f.stat().st_size>0,key+' evidence missing')
 # An import outside this directory is NOT locked. Humans must audit the closure.
 control_metrics(p,read(pathlib.Path(d)/p['controls_file']))
 return p

def freeze(d):
 d=pathlib.Path(d).resolve();require(not (d/'FREEZE.json').exists() and not (d/'HASHES.sha256').exists(),'refreeze forbidden: new study/version required')
 p=protocol(d);f=fileset(d);require(f,'nothing to freeze')
 manifest=''.join(h+'  '+k+'\n' for k,h in sorted(f.items())).encode()
 meta={'study_id':p['study_id'],'files':f,'manifest_sha256':digest(manifest),'local_created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'chronology':'NOT EXTERNALLY VERIFIED'}
 (d/'HASHES.sha256').write_bytes(manifest);(d/'FREEZE.json').write_bytes(dump(meta));return {'study_id':p['study_id'],'files':len(f),'freeze_sha256':digest((d/'FREEZE.json').read_bytes()),'science_status':'UNANCHORED'}

def verify_freeze(d):
 d=pathlib.Path(d).resolve();m=read(d/'FREEZE.json');require(fileset(d)==m['files'],'frozen file set or bytes changed')
 manifest=''.join(h+'  '+k+'\n' for k,h in sorted(m['files'].items())).encode()
 require((d/'HASHES.sha256').read_bytes()==manifest and digest(manifest)==m['manifest_sha256'],'manifest mismatch')
 p=protocol(d);require(m['study_id']==p['study_id'],'study mismatch');return p

def decision(p,units):
 require(isinstance(units,list) and len(units)>=p['min_units'],'too few independent units')
 ids=set();rows=[];lo,hi=p['metric_bounds']
 for r in units:
  require(set(r)=={'id','candidate','baselines'},'missing/extra unit fields')
  require(isinstance(r['id'],str) and r['id'] and r['id'] not in ids,'duplicate/invalid independent unit');ids.add(r['id'])
  require(set(r['baselines'])==set(p['baselines']),'missing/unregistered baseline')
  vals=[r['candidate'],*r['baselines'].values()];require(all(finite(x) and lo<=x<=hi for x in vals),'nonfinite or out-of-bound metric')
  strongest=max(r['baselines'].values());delta=r['candidate']-strongest
  rows.append({'id':r['id'],'delta':delta,'pass':delta>=p['margin']})
 n=len(rows);wins=sum(r['pass'] for r in rows);mean=sum(r['delta'] for r in rows)/n
 # Distribution-free conservative one-sided bound for independent bounded paired differences.
 lower=mean-(hi-lo)*math.sqrt(2*math.log(1/p['alpha'])/n)
 passed=(wins/n>=p['min_fraction'] and lower>=p['margin'])
 return {'threshold_met':passed,'n':n,'wins':wins,'fraction':wins/n,'mean_delta':mean,'lower_bound':lower,'rows':rows,'statistic':'Hoeffding lower bound; independent bounded units; no post-hoc unit regrouping'}

def bound_file(root,entry):
 require(set(entry)=={'path','sha256'},'bad file receipt')
 q=pathlib.Path(entry['path']);require(not q.is_absolute() and '..' not in q.parts,'unsafe receipt path')
 p=pathlib.Path(root)/q;require(p.is_file() and not p.is_symlink(),'receipt file missing')
 require(digest(p.read_bytes())==entry['sha256'],'receipt file hash mismatch');return p

def score(d,outcome_path,receipt_path):
 p=verify_freeze(d);o=read(outcome_path);receipt_path=pathlib.Path(receipt_path);r=read(receipt_path)
 require(o['study_id']==p['study_id'] and r['study_id']==p['study_id'],'wrong study')
 require(r['freeze_sha256']==digest((pathlib.Path(d)/'FREEZE.json').read_bytes()),'wrong freeze receipt')
 require(r['outcomes_sha256']==digest(pathlib.Path(outcome_path).read_bytes()),'wrong outcome receipt')
 require(r['external_anchor_verified'] is True and r['signed_tag_verified'] is True,'external anchor/signed tag unverified')
 require(isinstance(r['reviewer'],str) and r['reviewer'].strip(),'verification reviewer missing')
 for key in ['anchor_proof','tag_proof','data_manifest','environment_receipt','exposure_log']:
  bound_file(receipt_path.parent,r[key])
 require(stamp(r['anchor_verified_utc'])<stamp(r['first_exposure_utc']),'anchor did not precede exposure')
 exposures=read(bound_file(receipt_path.parent,r['exposure_log']))
 require(set(exposures['holdout_ids'])==set(p['data_ids']),'target exposure list mismatch')
 require(not set(p['data_ids'])&set(exposures['global_seen_before_anchor']),'global SEEN contamination')
 require(exposures['study_id']==p['study_id'],'wrong exposure study')
 manifest=read(bound_file(receipt_path.parent,r['data_manifest']))
 require(manifest['version'] and {x['id'] for x in manifest['records']}==set(p['data_ids']),'raw manifest version/IDs mismatch')
 require(len(manifest['records'])==len(p['data_ids']),'duplicate raw records')
 for record in manifest['records']:bound_file(receipt_path.parent,{'path':record['path'],'sha256':record['sha256']})
 require(exposures['first_exposure_utc']==r['first_exposure_utc'],'exposure time disagrees with receipt')
 require(o['admissibility_open'] is True,'admissibility CLOSED')
 require(set(o['raw_ids'])==set(p['data_ids']),'raw data IDs mismatch')
 require(isinstance(o['exclusions'],list),'exclusions not listed')
 used={u['id'] for u in o['units']};exc={x['id'] for x in o['exclusions']}
 require(all(set(x)=={'id','reason'} and x['reason'] for x in o['exclusions']),'bad exclusion reasons')
 require(len(exc)==len(o['exclusions']) and not used&exc and used|exc==set(p['data_ids']),'denominator/exclusions mismatch')
 expected=read(pathlib.Path(d)/p['controls_file'])
 require({x['id']:x['expected'] for x in o['controls']}=={x['id']:x['expected'] for x in expected},'control expectations changed after freeze')
 control_metrics(p,o['controls'])
 a=bound_file(receipt_path.parent,r['rerun_a']);b=bound_file(receipt_path.parent,r['rerun_b'])
 require(a.read_bytes()==pathlib.Path(outcome_path).read_bytes(),'rerun a not scored output')
 if r['reproduction']=='byte':require(a.read_bytes()==b.read_bytes(),'rerun byte mismatch')
 else:raise GateError('generic engine requires byte reproduction; tolerance needs separate frozen scorer')
 dec=decision(p,o['units']);cells=o['sensitivity'];require(isinstance(cells,list) and cells,'registered sensitivity cells absent')
 require(set(c['id'] for c in cells)==set(p.get('sensitivity_ids',[])) and len(cells)==len(p.get('sensitivity_ids',[])),'sensitivity cell set mismatch')
 flips=sum(decision(p,c['units'])['threshold_met']!=dec['threshold_met'] for c in cells)
 result={'artifacts':{'study':str(pathlib.Path(d).resolve()),'outcomes':str(pathlib.Path(outcome_path).resolve()),'receipts':str(receipt_path.resolve())},'study_id':p['study_id'],'verdict':'PASS-0' if dec['threshold_met'] else 'FAIL','sensitivity_flips':flips,'fragile':flips>p['max_sensitivity_flips'],'promotion_ceiling':'PASS-0; external scientific review required','freeze_sha256':r['freeze_sha256'],'outcomes_sha256':r['outcomes_sha256'],'receipt_sha256':digest(receipt_path.read_bytes()),'decision':dec}
 return result

def verify_sources(root=ROOT):
 root=pathlib.Path(root)
 entries=read(root/'GENEALOGY/UPSTREAM_BYTES.json')
 for r in entries:
  b=(root/r['local_path']).read_bytes();require(digest(b)==r['sha256'],'upstream bytes changed: '+r['local_path'])
  require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha'],'Git blob mismatch')
 require((root/'CORE/MATHEMATICS.md').read_bytes()==(root/'GENEALOGY/UPSTREAM/core.md').read_bytes(),'core differs from original')
 proto=(root/'GENEALOGY/UPSTREAM/ashes_CLAUDE.md').read_bytes();sec=b'## 1. Standing rules (non-negotiable)'+proto.split(b'## 1. Standing rules (non-negotiable)')[1].split(b'\n---')[0]
 require(sec==(root/'EPISTEMIC/R1_R15_EXACT.md').read_bytes(),'R1–R15 extract changed')
 locks=read(root/'EPISTEMIC/RELEASE_LOCKS.json')
 for name,sha in locks.items():require(digest((root/name).read_bytes())==sha,'protected release file changed: '+name)
 return {'source_files':len(entries),'protected_files':len(locks),'verified':'raw byte identity'}

def verify_ledger(root=ROOT):
 root=pathlib.Path(root);f=root/'EPISTEMIC/RESULT_LEDGER.jsonl';prev=ZERO;count=0;ids=set()
 for line in f.read_bytes().splitlines():
  require(line.strip(),'blank ledger record');e=json.loads(line);h=e.pop('entry_sha256');require(e['prev_sha256']==prev,'ledger chain broken')
  require(digest(dump(e))==h,'ledger bytes altered');require(e['entry_id'] not in ids,'duplicate ledger entry');ids.add(e['entry_id']);prev=h;count+=1
 require(read(root/'EPISTEMIC/ledger_head.json')=={'count':count,'head':prev},'ledger head mismatch')
 return {'count':count,'head':prev,'trust_limit':'verify head against external trusted anchor'}

def main():
 ap=argparse.ArgumentParser();s=ap.add_subparsers(dest='cmd',required=True)
 for name in ['freeze','verify']:q=s.add_parser(name);q.add_argument('study')
 q=s.add_parser('score');q.add_argument('study');q.add_argument('outcomes');q.add_argument('receipts')
 s.add_parser('sources');s.add_parser('ledger');args=ap.parse_args()
 try:
  if args.cmd=='freeze':r=freeze(args.study)
  elif args.cmd=='verify':verify_freeze(args.study);r={'integrity':'OK','chronology':'requires external verification'}
  elif args.cmd=='score':r=score(args.study,args.outcomes,args.receipts)
  elif args.cmd=='sources':r=verify_sources()
  else:r=verify_ledger()
  print(json.dumps(r,sort_keys=True,indent=2,allow_nan=False))
 except (GateError,KeyError,FileNotFoundError,ValueError) as e:
  print(json.dumps({'gate':'CLOSED','reason':str(e)}));return 2
 return 0
if __name__=='__main__':sys.exit(main())
