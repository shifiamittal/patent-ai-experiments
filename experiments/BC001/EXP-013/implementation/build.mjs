import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const data=JSON.parse(await fs.readFile(new URL('./ranked.json',import.meta.url),'utf8'));
const outputDir=new URL('../outputs/bc001_v1/',import.meta.url);
await fs.mkdir(outputDir,{recursive:true});
const w=Workbook.create();
const full=w.worksheets.add('Full Ranking');
const top=w.worksheets.add('Top 100 Evidence');
const headers=['V1 rank','Record ID','Relevance score (0–100)','Predicted relevance: H, M+, M, L or N','Short ranking reason'];
const eh=['V1 rank','Record ID','Relevance score','Predicted relevance',...Array.from({length:8},(_,i)=>`F${i+1}`),'Best supporting title/abstract text','One-sentence explanation of the feature combination','Limitation or uncertainty'];
full.getRange('A1').values=[['BC001 V1 — Blinded technical relevance ranking']];
full.getRange('A2').values=[['3,238 supplied families. Titles and abstracts only. No external identity lookup.']];
full.getRange('A3').values=[['H ≥75; M+ 55–74; M 30–54; L 10–29; N 0–9. Scores express screening priority, not patentability.']];
full.getRange('A4').values=[['Primary combinations and clearer evidence break score ties. Identical-content ties are interchangeable.']];
top.getRange('A1').values=[['BC001 V1 — Top 100 evidence']];
top.getRange('A2').values=[['E = explicit; I = inferred (basis in limitation); A = absent/not established. Optional embodiments count as explicit.']];
top.getRange('A3').values=[['F1 firearm; F2 biometrics; F3 authorization control; F4 location restriction; F5 tracking/data; F6 central integration; F7 use purpose; F8 danger unlocking.']];
top.getRange('A4').values=[['F5 includes biometric collection; it need not imply a usage log. F6 limitations distinguish central integration from alerts.']];
full.getRange(`A5:E${data.length+5}`).values=[headers,...data.map(r=>[r.rank,r.id,r.score,r.category,r.reason])];
top.getRange('A5:O105').values=[eh,...data.slice(0,100).map(r=>[r.rank,r.id,r.score,r.category,...r.f,r.evidence,r.explain.startsWith('Biometric user verification controls')?'Biometric user verification controls firearm firing or a firearm-attached safety lock.':r.explain,r.lim])];
for(const [s,end,rows,name] of [[full,'E',3243,'FullRankingTable'],[top,'O',105,'TopEvidenceTable']]){
 s.showGridLines=false;s.tabColor='#243C5A';
 s.getRange(`A1:${end}${rows}`).format.font={name:'Arial',size:10,color:'#17283B'};
 s.getRange(`A1:${end}${rows}`).format.verticalAlignment='top';
 s.getRange('A1').format.font={name:'Arial',size:14,bold:true,color:'#243C5A'};
 s.getRange(`A1:${end}1`).format.rowHeight=24;
 s.getRange(`A2:${end}4`).format.rowHeight=19;
 s.getRange(`A2:${end}4`).format.font={name:'Arial',size:10,color:'#4E6072'};
 s.getRange(`A5:${end}5`).format={fill:'#243C5A',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center',rowHeight:42};
 s.getRange(`A6:${end}${rows}`).format.wrapText=true;
 s.getRange(`A6:D${rows}`).format.horizontalAlignment='center';
 s.getRange(`A6:A${rows}`).setNumberFormat('0');s.getRange(`C6:C${rows}`).setNumberFormat('0');
 s.getRange(`A1:A${rows}`).format.columnWidth=9;
 s.getRange(`B1:B${rows}`).format.columnWidth=25;
 s.getRange(`C1:C${rows}`).format.columnWidth=17;
 s.getRange(`D1:D${rows}`).format.columnWidth=19;
 s.tables.add(`A5:${end}${rows}`,true,name);
 s.freezePanes.freezeRows(5);
 s.freezePanes.freezeColumns(2);
}
full.getRange('E1:E3243').format.columnWidth=105;
full.getRange('A6:E3243').format.rowHeight=44;
top.getRange('E1:L105').format.columnWidth=5;
top.getRange('E6:L105').format.horizontalAlignment='center';
top.getRange('M1:M105').format.columnWidth=105;
top.getRange('N1:N105').format.columnWidth=63;
top.getRange('O1:O105').format.columnWidth=70;
for(let i=0;i<100;i++){
 const r=data[i];
 const lines=Math.max(Math.ceil(r.evidence.length/128)+3,Math.ceil(r.explain.length/72)+2,Math.ceil(r.lim.length/80)+2);
 top.getRange(`A${i+6}:O${i+6}`).format.rowHeight=Math.min(409,Math.max(90,lines*12));
}
for(const mark of ['E','I','A']) top.getRange('E6:L105').conditionalFormats.add('containsText',{text:mark,format:{fill:mark==='E'?'#E3EFE8':mark==='I'?'#FFF1CE':'#F1F3F5',font:{color:mark==='I'?'#79530B':'#243C5A'}}});
w.recalculate();
console.log((await w.inspect({kind:'table',range:'Full Ranking!A5:E8',tableMaxRows:4,tableMaxCols:5,maxChars:1600})).ndjson);
console.log((await w.inspect({kind:'table',range:'Top 100 Evidence!A5:L7',tableMaxRows:3,tableMaxCols:12,maxChars:1600})).ndjson);
const x=await SpreadsheetFile.exportXlsx(w);await x.save(fileURLToPath(new URL('BC001_V1_Ranked_Output.xlsx',outputDir)));
for(const [s,range,file] of [['Full Ranking','A1:E10','full_preview.png'],['Top 100 Evidence','A1:L8','evidence_labels.png'],['Top 100 Evidence','M5:O8','evidence_text.png']]){
 const b=await w.render({sheetName:s,range,scale:1,format:'png'});
 await fs.writeFile(new URL(file,outputDir),new Uint8Array(await b.arrayBuffer()));
}
console.log('EXPORTED',data.length,'records; 100 evidence rows.');
