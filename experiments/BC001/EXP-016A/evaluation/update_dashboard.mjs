import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';

const repo = process.argv[2];
const mode = process.argv[3] ?? 'inspect';
const file = path.join(repo, 'Patent_AI_Experiment_Dashboard_Canonical.xlsx');
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const outDir = path.join(process.env.TEMP, 'exp016a-dashboard');
if (mode === 'inspect') {
  console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:3000})).ndjson);
  const preview = await wb.render({sheetName:'Dashboard',range:'A1:H24',scale:1,format:'png'});
  await fs.writeFile(path.join(outDir,'dashboard-before.png'),new Uint8Array(await preview.arrayBuffer()));
} else {
  const m = JSON.parse(await fs.readFile(path.join(repo,'experiments/BC001/EXP-016A/evaluation/metrics.json'),'utf8'));
  const row = JSON.parse(await fs.readFile(path.join(repo,'experiments/BC001/EXP-016A/evaluation/dashboard-row.json'),'utf8'));
  const log = wb.worksheets.getItem('Experiment Log');
  if (log.getRange('A19').values[0][0]) throw new Error('Expected empty experiment row 19');
  log.getRange('A19:V19').copyFrom(log.getRange('A18:V18'),'all');
  const values = row.values.map(v => v === '' ? null : v);
  values[1] = new Date('2026-09-17T00:00:00Z');
  log.getRange('A19:V19').values = [values];
  log.getRange('B19').setNumberFormat('yyyy-mm-dd');
  log.getRange('L19:M19').setNumberFormat('0%');
  log.getRange('P19').setNumberFormat('0.0');
  log.getRange('A19:V19').format.wrapText = true;
  log.getRange('A19:V19').format.rowHeight = 70;
  log.getRange('A19:V19').format.verticalAlignment = 'center';
  const versions = wb.worksheets.getItem('Component Versions');
  if (versions.getRange('A9').values[0][0]) throw new Error('Expected empty component row 9');
  versions.getRange('A9:G9').copyFrom(versions.getRange('A6:G6'),'all');
  versions.getRange('A9:G9').values = [['Relevance Scorer (challenger)','rs_v0.3_feature_aware_ta','REJECT; challenger only','Feature-aware title/abstract ranking','EXP-016A','No','Recall@20 1/10; median GOLD rank 142.5. Rule-based extraction; no promotion.']];
  versions.getRange('A9:G9').format.wrapText = true;
  versions.getRange('A9:G9').format.rowHeight = 50;
  versions.getRange('A9:G9').format.verticalAlignment = 'center';
  const dash = wb.worksheets.getItem('Dashboard');
  dash.getRange('B8').values = [['EXP-016A']];
  dash.getRange('A86:H86').format.fill = '#D9EAF7';
  dash.getRange('A86:H86').merge();
  dash.getRange('A86').values = [['EXP-016A — feature-aware title/abstract ranking']];
  dash.getRange('A86:H86').format.font = {name:'Carlito',size:11,bold:true};
  dash.getRange('A87:H87').merge();
  dash.getRange('A87').values = [['REJECT — Recall@20 fell below its guardrail; median retrieved-GOLD rank worsened by more than 10%.']];
  dash.getRange('A87:H87').format.font = {name:'Carlito',size:11};
  dash.getRange('A87:H87').format.rowHeight = 24;
  dash.getRange('A89:B89').values = [['Metric','EXP-013']];
  dash.getRange('D89:E89').values = [['EXP-016A','Change']];
  for (const range of ['A89:B89','D89:E89']) dash.getRange(range).format = {fill:'#4472C4',font:{name:'Carlito',size:11,bold:true,color:'#FFFFFF'}};
  const comp = [
    ['Recall@20',0.2,m.recall_at_20.value], ['Recall@50',0.2,m.recall_at_50.value],
    ['Recall@100',0.4,m.recall_at_100.value], ['Recall@200',0.5,m.recall_at_200.value],
    ['Median GOLD rank',90.5,m.median_rank_retrieved_gold],
  ];
  for (let i=0;i<comp.length;i++) {
    const n=90+i;
    dash.getRange(`A${n}:B${n}`).values = [[comp[i][0],comp[i][1]]];
    dash.getRange(`D${n}`).values = [[comp[i][2]]];
    dash.getRange(`E${n}`).formulas = [[i<4 ? `=(D${n}-B${n})*100` : `=D${n}-B${n}`]];
  }
  dash.getRange('B90:B93').setNumberFormat('0%');
  dash.getRange('D90:D93').setNumberFormat('0%');
  dash.getRange('E90:E93').setNumberFormat('0" pp"');
  dash.getRange('B94').setNumberFormat('0.0');
  dash.getRange('D94:E94').setNumberFormat('0.0');
  dash.getRange('A89:E94').format.rowHeight = 22;
  const notes = [
    'Recall denominator: GOLD-10. Median: six retrieved GOLD families. All 3,238 records ranked exactly once.',
    'Ranking frozen before private evaluation. Original key unavailable; all six reconstructed GOLD mappings are exact.',
    'Deterministic rule extraction; evidence judgments are not analyst labels. Component remains a challenger.',
    'Source: experiments/BC001/EXP-016A/evaluation/evaluation.md',
  ];
  for (let i=0;i<notes.length;i++) {
    const n=96+i;
    dash.getRange(`A${n}:H${n}`).merge();
    dash.getRange(`A${n}`).values = [[notes[i]]];
    dash.getRange(`A${n}:H${n}`).format.font = {name:'Carlito',size:11};
    dash.getRange(`A${n}:H${n}`).format.rowHeight = 22;
  }
  wb.recalculate();
  console.log((await wb.inspect({kind:'region',sheetId:'Dashboard',range:'A86:H99',maxChars:5000})).ndjson);
  console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:20},maxChars:2000})).ndjson);
  for (const [sheetName,range,filename] of [
    ['Dashboard','A86:H99','dashboard-after.png'],
    ['Experiment Log','A19:K19','log-left.png'],
    ['Experiment Log','L19:V19','log-right.png'],
    ['Component Versions','A9:G9','component-after.png'],
  ]) {
    const preview=await wb.render({sheetName,range,scale:1,format:'png'});
    await fs.writeFile(path.join(outDir,filename),new Uint8Array(await preview.arrayBuffer()));
  }
  const output=await SpreadsheetFile.exportXlsx(wb);
  await output.save(path.join(outDir,'dashboard-updated.xlsx'));
  console.log('Exported updated dashboard to staging for preservation verification.');
}
