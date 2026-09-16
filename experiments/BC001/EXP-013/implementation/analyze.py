import json,re,pathlib
p=pathlib.Path(__file__).parent
rows=json.loads((p/'input.json').read_text(encoding='utf-8'))[1:]
assert len(rows)==3238 and len(set(x[0] for x in rows))==3238
def hit(t,s): return bool(re.search(s,t,re.I))
out=[]
for id,title,abstract in rows:
 t=title+' '+(abstract or '')
 gun=hit(t,r'firearm|fire arm|handgun|pistol|rifle|\bgun\b|weapon|shooting|firing|trigger')
 bio=hit(t,r'biometr|fingerprint|finger print|palm.?print|palm.?vein|iris|retina|facial recognition|face recognition|heart.?rate|physiolog')
 control=hit(t,r'lock|unlock|disabl|enabl|authoriz|authent|prevent.{0,30}(fir|discharg)|permission|restrict|recognition|identif')
 geo=hit(t,r'geofenc|geo.?locat|GPS|geographic|positioning|location')
 log=hit(t,r'track|trac(e|ing|eability)|logg|record|monitor|collect|data|sensor')
 exclude=hit(title,r'weld|spray|charg|toy|simulat|game|cabinet|safe\b|locker|storage|box|rack|holster')
 pre=(30*gun+30*(gun and bio)+15*(gun and control)+8*(gun and geo)+5*(gun and log)-35*exclude)
 out.append(dict(id=id,title=title,abstract=abstract or '',pre=pre,gun=gun,bio=bio,control=control,geo=geo,log=log,exclude=exclude))
out.sort(key=lambda x:(-x['pre'],x['title'],x['abstract']))
(p/'screen.json').write_text(json.dumps(out,ensure_ascii=False),encoding='utf-8')
(p/'candidates.txt').write_text('\n\n'.join(f"{i+1} {r['id']} [{r['pre']}] {r['title']}\n{r['abstract']}" for i,r in enumerate(out) if r['pre']>=58),encoding='utf-8')
print('All rows processed:',len(out),'Candidate count:',sum(r['pre']>=58 for r in out))
print('\n'.join(f"{i+1} [{r['pre']}] {r['title']}" for i,r in enumerate(out[:230])))
