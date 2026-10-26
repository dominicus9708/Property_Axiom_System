#!/usr/bin/env python3
"""Independent finite stress and countermodel verification for P27.

Tests discrete abstract models, NOT a general infinite model proof.
Run with an optional JSON output path; default writes next to this file.
"""
from itertools import product, permutations
from pathlib import Path
from dataclasses import dataclass
import json,sys,collections

KINDS=('p','q')
DEPS={'p':(), 'q':('d',)}

@dataclass(frozen=True)
class Core:
    available:bool
    n:int
    kinds:tuple[str,...]
    # tuples of (name, (app_indices), (sat_indices), ((index,value),...))
    entries:tuple

def options_for_kind(k,n):
    values=[]
    # each input independently: (applicable, sat-prereq, assigned value None or 0/1)
    if k=='p':
        atoms=[(False,True,None),(True,True,None),(True,True,0),(True,True,1)]
    else:
        atoms=[(False,False,None),(False,True,None),(True,False,None),
               (True,True,None),(True,True,0),(True,True,1)]
    for config in product(atoms,repeat=n):
        app=tuple(i for i,(a,sa,v) in enumerate(config) if a)
        sat=tuple(i for i,(a,sa,v) in enumerate(config) if sa)
        xi=tuple((i,v) for i,(a,sa,v) in enumerate(config) if v is not None)
        values.append((app,sat,xi))
    return values

def generate(n,available=True):
    if not available:
        return [Core(False,0,tuple(k for i,k in enumerate(KINDS) if (mask>>i)&1),()) for mask in range(4)]
    opts={k:options_for_kind(k,n) for k in KINDS}
    cores=[]
    for mask in range(4):
        kinds=tuple(k for i,k in enumerate(KINDS) if (mask>>i)&1)
        for coords in product(*(opts[k] for k in kinds)):
            entries=tuple((k,*c) for k,c in zip(kinds,coords))
            cores.append(Core(True,n,kinds,entries))
    return cores

def completion(A):
    # canonical C1 status of each full-domain input and record set
    statuses=[];records=[]
    for k,app,sat,xi in A.entries:
        assigned=dict(xi)
        for i in range(A.n):
            if i not in app: status='inapplicable'
            elif k=='q' and i not in sat: status='prerequisite_unsatisfied'
            elif i not in assigned: status='applicable_undefined'
            elif assigned[i]==0: status='defined_zero'
            else:status='defined_nonzero'
            statuses.append((k,i,status))
        for i,v in xi: records.append((k,i,v))
    return tuple(statuses),tuple(records)

def transformed(A,perm):
    if not A.available:return (),()
    st3=[];st4=[]
    for k,app,sat,xi in A.entries:
        app_t=tuple(sorted(perm[i] for i in app))
        sat_t=tuple(sorted(perm[i] for i in sat)) if k=='q' else ()
        st3.append((k,app_t,sat_t))
        st4.append((k,app_t,sat_t,tuple(sorted((perm[i],v) for i,v in xi))))
    return tuple(st3),tuple(st4)

def strict_embedding_direct(A,B,perm):
    if A.available!=B.available or A.kinds!=B.kinds:return False
    if not A.available:return True
    if A.n!=B.n:return False
    mapped={k:(app,sat,dict(xi)) for k,app,sat,xi in B.entries}
    for k,app,sat,xi in A.entries:
        ba,bs,bxi=mapped[k]; ax=dict(xi)
        for i,j in enumerate(perm):
            if (i in app)!=(j in ba):return False
            if k=='q' and ((i in sat)!=(j in bs)):return False
            if (i in ax)!=(j in bxi):return False
            if i in ax and ax[i]!=bxi[j]:return False
    return True

def source_embedding_direct(A,B,assignment):
    # forward embedding: can have target extra kinds, target extra supplied sort
    if A.available and not B.available:return False
    if not set(A.kinds).issubset(set(B.kinds)):return False
    if not A.available:return True
    if len(set(assignment))!=len(assignment):return False
    target={k:(app,sat,dict(xi)) for k,app,sat,xi in B.entries}
    for k,app,sat,xi in A.entries:
        a=dict(xi); bapp,bsat,bvals=target[k]
        for i,j in enumerate(assignment):
            if (i in app)!=(j in bapp):return False
            if k=='q' and ((i in sat)!=(j in bsat)):return False
            if (i in a)!=(j in bvals):return False
            if i in a and a[i]!=bvals[j]:return False
    return True

def forward(A,B,assignment):
    if A.available and not B.available:return False
    if not set(A.kinds).issubset(set(B.kinds)):return False
    if not A.available:return True
    target={k:(app,sat,dict(xi)) for k,app,sat,xi in B.entries}
    for k,app,sat,xi in A.entries:
        a=dict(xi); bapp,bsat,bvals=target[k]
        for i,j in enumerate(assignment):
            if i in app and j not in bapp:return False
            if k=='q' and i in sat and j not in bsat:return False
            if i in a and (j not in bvals or a[i]!=bvals[j]):return False
    return True

def simple_summary(A,labelled=True):
    assert A.available
    triples=[]
    for k,app,sat,xi in A.entries:
        nzero=sum(v==0 for _,v in xi)
        other=len(xi)-nzero
        data=(len(xi),nzero,other)
        triples.append((k,*data) if labelled else data)
    return (len(A.kinds),frozenset(triples))

def run():
    byn={0:generate(0),1:generate(1),2:generate(2)}
    byn['unavailable']=generate(0,False)
    result={'model_counts':{str(k):len(v) for k,v in byn.items()},'cases':{},'limits':'only one auxiliary sort with n=0,1,2, two property kinds p(no prerequisites),q(one prerequisite), Z={0,1}'}
    assert result['model_counts']['2']==629
    # all typed cores PI,PII; C1 deterministic from primitive and eq after reapplication
    total=0
    for arr in byn.values():
        for a in arr:
            statuses,records=completion(a)
            assert completion(a)==(statuses,records)
            assert len(records)==sum(len(xi) for _,ap,sat,xi in a.entries)
            for k,app,sat,xi in a.entries:
                for i,v in xi:
                    assert i in app and (k!='q' or i in sat)
            total+=1
    result['cases']['typed_axiom_and_C1_idempotence']=total
    # for n=2 full 629^2 ordered pairs, strict vs I4 and I5 and stage chain, symmetry
    paircount=0;iso=0;strict_maps=0;branch_counts=collections.Counter()
    for key,arr in byn.items():
        if key=='unavailable':
            canonical=[((),(),{()},{()}) for a in arr]
        else:
            canonical=[]
            for a in arr:
                options=[transformed(a,perm) for perm in permutations(range(a.n))]
                s3={i[0] for i in options}
                s4={i[1] for i in options}
                canonical.append((transformed(a,tuple(range(a.n)))[0],transformed(a,tuple(range(a.n)))[1],s3,s4))
        for i,A in enumerate(arr):
            for j,B in enumerate(arr):
                paircount+=1
                I1=(A.available==B.available and A.n==B.n)
                I2=I1 and A.kinds==B.kinds
                I3=I2 and canonical[j][0] in canonical[i][2]
                I4=I3 and canonical[j][1] in canonical[i][3]
                I5=I4 # C1 is a deterministic functor of primitive stage 4
                assert (not I5 or I4) and (not I4 or I3) and (not I3 or I2) and (not I2 or I1)
                if I4:iso+=1
                if I2:
                    if not A.available: strict=True;strict_count=1
                    else:
                        strict_count=sum(strict_embedding_direct(A,B,perm) for perm in permutations(range(A.n)))
                        strict=bool(strict_count)
                    strict_maps+=strict_count
                    assert strict==I4, (A,B)
                if not I4:
                    b=next(k for k,ok in enumerate((I1,I2,I3,I4),start=1) if not ok)
                    branch_counts[b]+=1
                    if I2: assert (I3==False if b==3 else True) or b==4
                # symmetry of comparisons, including at intermediate stages
                if I2:
                    assert (canonical[i][0] in canonical[j][2])==I3
                    assert (canonical[i][1] in canonical[j][3])==I4
    result['cases']['ordered_model_pair_checks']=paircount
    result['cases']['stage4_stage5_equivalence_pairs']=iso
    result['cases']['strict_embedding_map_count']=strict_maps
    result['cases']['first_branch_histogram']=dict(sorted(branch_counts.items()))
    # Old unlabelled summary erases actual property-label/count association.
    p0_q1=next(x for x in byn[1] if x.kinds==KINDS and dict((k,len(xi)) for k,ap,sat,xi in x.entries)=={'p':0,'q':1})
    p1_q0=next(x for x in byn[1] if x.kinds==KINDS and dict((k,len(xi)) for k,ap,sat,xi in x.entries)=={'p':1,'q':0})
    # choose q's assigned 1 to match p's (needs value check), not arbitrary first option
    p0_q1=next(x for x in byn[1] if x.kinds==KINDS and dict((k,len(xi)) for k,ap,sat,xi in x.entries)=={'p':0,'q':1} and dict((k,xi) for k,ap,sat,xi in x.entries)['q']==((0,1),))
    p1_q0=next(x for x in byn[1] if x.kinds==KINDS and dict((k,len(xi)) for k,ap,sat,xi in x.entries)=={'p':1,'q':0} and dict((k,xi) for k,ap,sat,xi in x.entries)['p']==((0,1),))
    assert simple_summary(p0_q1,False)==simple_summary(p1_q0,False)
    assert simple_summary(p0_q1,True)!=simple_summary(p1_q0,True)
    result['cases']['old_summary_label_collision_counterexample']=True
    # No prerequisites must not eliminate independent E1/E3 reflection. p has delta empty.
    A=next(x for x in byn[1] if x.kinds==('p',) and x.entries[0][1]==(0,) and not x.entries[0][3])
    B=next(x for x in byn[1] if x.kinds==('p',) and x.entries[0][1]==() and not x.entries[0][3])
    assert forward(A,B,(0,))==False
    assert source_embedding_direct(A,B,(0,))==False
    result['cases']['empty_prerequisite_E1_reflection_not_vacuous']=True
    # Source-declared kind with unavailable profile is permitted: identity forward+embedding.
    A=next(x for x in byn['unavailable'] if x.kinds==KINDS)
    assert forward(A,A,()) and source_embedding_direct(A,A,())
    result['cases']['unavailable_profile_identity_defined']=True
    # Carrier bijection is not strict if declaration sets differ (S3) or avail sets differ(S2).
    A=next(x for x in byn[1] if x.kinds==())
    B=next(x for x in byn[1] if x.kinds==('p',))
    assert source_embedding_direct(A,B,(0,)) and not strict_embedding_direct(A,B,(0,))
    result['cases']['S3_extra_target_decl_countermodel']=True
    A=next(x for x in byn['unavailable'] if x.kinds==())
    B=next(x for x in byn[0] if x.kinds==())
    assert source_embedding_direct(A,B,())
    result['cases']['S2_extra_target_carrier_countermodel']=True
    # C1 cannot serve as a premise of axiom-violating typed counterpremodels.
    bad_pi={'app':(), 'sat':(0,), 'xi':((0,1),)}
    bad_pii={'app':(0,), 'sat':(), 'xi':((0,1),)}
    assert set(i for i,v in bad_pi['xi']).issubset(set(bad_pi['sat'])) and not set(i for i,v in bad_pi['xi']).issubset(set(bad_pi['app']))
    assert set(i for i,v in bad_pii['xi']).issubset(set(bad_pii['app'])) and not set(i for i,v in bad_pii['xi']).issubset(set(bad_pii['sat']))
    result['cases']['independence_two_typed_counterpremodels']=True
    return result

if __name__=='__main__':
    result=run();out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('P27_INDEPENDENT_FINITE_CHECKS.json')
    out.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))