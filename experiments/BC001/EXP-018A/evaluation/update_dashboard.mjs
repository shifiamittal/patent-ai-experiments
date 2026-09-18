import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const repo=process.argv[2], mode=process.argv[3]??'inspect';
const dir=path.join(repo,'outputs/exp018a-dashboard');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path.join(repo,'Patent_AI_Experiment_Dashboard_Canonical.xlsx')));
if(mode==='inspect') {
  console.log((await wb.inspect({kind:'region',sheetId:'Dashboard',range:'A1:H24',maxChars:4500})).ndjson);
  const p=await wb.render({sheetName:'Dashboard',range:'A86:H99',scale:1,format:'png'});
  await fs.writeFile(path.join(dir,'before.png'),new Uint8Array(await p.arrayBuffer()));
} else {
  const row=JSON.parse(await fs.readFile(path.join(repo,'experiments/BC001/EXP-018A/evaluation/dashboard-row.json'),'utf8'));
  const log=wb.worksheets.getItem('Experiment Log');
  if(log.getRange('A21').values[0][0]) throw new Error('Expected empty row 21');
  log.getRange('A21:V21').copyFrom(log.getRange('A19:V19'),'all');
  const values=row.values.map(v=>v===''?null:v);values[1]=new Date('2026-09-18T00:00:00Z');
  log.getRange('A21:V21').values=[values];
  log.getRange('B21').setNumberFormat('yyyy-mm-dd');
  log.getRange('L21:M21').setNumberFormat('0%');
  log.getRange('P21').setNumberFormat('0.0');
  log.getRange('A21:V21').format.rowHeight=100;
  log.getRange('A21:V21').format.verticalAlignment='center';
  const comp=wb.worksheets.getItem('Component Versions');
  comp.getRange('A10:G10').copyFrom(comp.getRange('A9:G9'),'all');
  comp.getRange('A10:G10').values=[['Relevance Scorer','rs_v0.4_extraction_gate_repair_ta','PROMOTE; BC001 TA champion','Extraction/gating repair; fixed scoring','EXP-018A','Yes','Same recall as EXP-013; median 55. BC001 title/abstract only.']];
  comp.getRange('A10:G10').format.rowHeight=65;
  comp.getRange('A10:G10').format.verticalAlignment='center';
  const d=wb.worksheets.getItem('Dashboard');
  d.getRange('B6').values=[['RUN-012 + EXP-018A + evidence assist']];
  d.getRange('B7').values=[['EXP-018A — BC001 TA only']];
  d.getRange('B8').values=[['EXP-018A']];
  d.getRange('A123:H123').merge();
  d.getRange('A123').values=[['EXP-018A — Title/abstract extraction and gating repair']];
  d.getRange('A123:H123').format={fill:'#D9EAF7',font:{name:'Carlito',size:11,bold:true},rowHeight:25};
  d.getRange('A124:H124').merge();
  d.getRange('A124').values=[['PROMOTE — recall matches EXP-013; median GOLD rank improves from 90.5 to 55.']];
  d.getRange('A124:H124').format.rowHeight=25;
  d.getRange('A126:B126').values=[['Metric','EXP-013']];
  d.getRange('D126:E126').values=[['EXP-016A','EXP-018A']];
  for(const range of ['A126:B126','D126:E126']) d.getRange(range).format={fill:'#4472C4',font:{name:'Carlito',size:11,bold:true,color:'#FFFFFF'},rowHeight:23};
  d.getRange('A127:B131').values=[['Recall@20',.2],['Recall@50',.2],['Recall@100',.4],['Recall@200',.5],['Median GOLD rank',90.5]];
  d.getRange('D127:E131').values=[[.1,.2],[.2,.2],[.3,.4],[.3,.5],[142.5,55]];
  d.getRange('B127:B130').setNumberFormat('0%');d.getRange('D127:E130').setNumberFormat('0%');
  d.getRange('B131').setNumberFormat('0.0');d.getRange('D131:E131').setNumberFormat('0.0');
  d.getRange('A127:E131').format.rowHeight=23;
  const notes=[
    'Recall denominator: GOLD-10. Median: six retrieved families. Top-20 overlap: EXP-013 8/20; EXP-016A 13/20.',
    'Affected records: outcomes 7; relationships 61; mechanism 111; storage 63. Sequential counts overlap.',
    'All preservation checks passed. Fixed scoring; 66 tests. Ranking committed before private mapping access.',
    'Mechanism-general; validated on BC001 only. Diagnosis-informed repair; no cross-domain validation.',
    'Individual GOLD ranks remain mixed. Sparse evidence and translated container terminology remain limits.',
    'Source: experiments/BC001/EXP-018A/evaluation/evaluation.md'
  ];
  for(let i=0;i<notes.length;i++) {const r=133+i;d.getRange(`A${r}:H${r}`).merge();d.getRange(`A${r}`).values=[[notes[i]]];d.getRange(`A${r}:H${r}`).format={font:{name:'Carlito',size:11},rowHeight:24};}
  wb.recalculate();
  console.log((await wb.inspect({kind:'region',sheetId:'Dashboard',range:'A123:H138',maxChars:4000})).ndjson);
  console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},maxChars:1500})).ndjson);
  for(const [sheetName,range,name] of [['Dashboard','A123:H138','after'],['Dashboard','A4:H10','current'],['Experiment Log','A21:K21','log-left'],['Experiment Log','L21:V21','log-right'],['Component Versions','A10:G10','component']]) {
    const p=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(path.join(dir,name+'.png'),new Uint8Array(await p.arrayBuffer()));
  }
  await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(dir,'dashboard-updated.xlsx'));
}
