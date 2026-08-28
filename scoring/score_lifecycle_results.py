#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def rows(path):
    return [json.loads(x) for x in Path(path).read_text(encoding='utf-8').splitlines() if x.strip()]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cases',required=True); p.add_argument('--results',required=True); p.add_argument('--out')
    a=p.parse_args(); cases={x['id']:x for x in rows(a.cases)}; details=[]
    for r in rows(a.results):
        c=cases.get(r.get('case_id'))
        missing=[] if not c else [g for g in c['required_gates'] if r.get('gates',{}).get(g) is not True]
        autonomous=r.get('operator_interventions',0)==0 and r.get('mode') in {'model_direct','model_asb_api','model_asb_ui'}
        details.append({'case_id':r.get('case_id'),'passed':bool(c) and not missing,'missing_gates':missing,'autonomous':autonomous})
    passed=sum(x['passed'] for x in details)
    report={'total_cases':len(cases),'results_received':len(details),'passed':passed,'pass_rate':passed/len(cases) if cases else 0,'details':details}
    text=json.dumps(report,ensure_ascii=False,indent=2)
    if a.out: Path(a.out).write_text(text+chr(10),encoding='utf-8')
    print(text)

if __name__=='__main__': main()
