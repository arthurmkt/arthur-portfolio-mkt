// Prints de uma página em tamanho de celular (e de computador), sem Playwright: só o Chrome instalado.
// Caminho do Chrome: padrão do macOS; em Linux/Windows defina CHROME_PATH.
// Uso:
//   node teste-celular.mjs <url-base> "#parte1,#parte2" [largura] [altura] [pasta-saida] [--lento]
//   ex.: node teste-celular.mjs http://localhost:8766/site.html "#topo,#provas" 393 852 prints
// Tamanhos que valem a pena: 393x852 (iPhone 14/15, o mais comum) · 375x667 (iPhone SE, o mais baixo) · 1440x900 (computador)
// --lento simula 4G (2,5 MB/s, 40 ms): mostra se a página trava esperando download.
// --inteira rola a página toda e tira uma tela a cada ~90% de altura (LP de uma página só): mostra o que a pessoa vê, tela por tela.
//   (o print "de página inteira" do Chrome repete pedaços com elementos fixos e 100vh — não usar)
// Aprendizados (nov/2026):
//  - o perfil temporário do Chrome é APAGADO no fim; sem isso cada rodada deixa ~150 MB e o disco enche;
//  - cada parte é aberta do zero (navegação nova), para um estado não contaminar o próximo print;
//  - o print sai em 2x (tela de celular real); para revisar muitas telas, monte uma folha lado a lado.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync, rmSync, mkdirSync } from 'node:fs';
import os from 'node:os';

const [base, partes = '', L = '393', A = '852', saida = 'prints'] = process.argv.slice(2);
const lento = process.argv.includes('--lento'), inteira = process.argv.includes('--inteira');
if (!base) { console.log('uso: node teste-celular.mjs <url> "#a,#b" [largura] [altura] [pasta] [--lento] [--inteira]'); process.exit(1); }
const W = +L, H = +A, celular = W < 900, PORTA = 9300 + Math.floor(Math.random() * 600);
const dir = mkdtempSync(os.tmpdir() + '/teste-celular-');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const chrome = spawn(process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', `--remote-debugging-port=${PORTA}`, `--user-data-dir=${dir}`, `--window-size=${W},${H}`, '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
const limpa = () => { try { chrome.kill(); } catch (e) {} setTimeout(() => { try { rmSync(dir, { recursive: true, force: true }); } catch (e) {} }, 600); };
process.on('exit', limpa);

let alvo; for (let i = 0; i < 40 && !alvo; i++) { try { alvo = (await (await fetch(`http://127.0.0.1:${PORTA}/json`)).json()).find(t => t.type === 'page'); } catch (e) {} if (!alvo) await sleep(250); }
const ws = new WebSocket(alvo.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}, erros = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d); delete pend[d.id]; }
  if (d.method === 'Runtime.exceptionThrown') erros.push((d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text || '').split('\n')[0]); };
const cdp = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });

await cdp('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: celular });
if (celular) await cdp('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
await cdp('Runtime.enable'); await cdp('Page.enable'); await cdp('Network.enable');
if (lento) await cdp('Network.emulateNetworkConditions', { offline: false, latency: 40, downloadThroughput: 2.5e6, uploadThroughput: 1e6 });
mkdirSync(saida, { recursive: true });

const lista = partes ? partes.split(',') : [''];
for (const [n, p] of lista.entries()) {
  const t0 = Date.now();
  await cdp('Page.navigate', { url: base + p }); await sleep(lento ? 9000 : 6000);
  const nome = `${saida}/${String(n).padStart(2, '0')}-${(p || 'inicio').replace(/[^\w-]/g, '')}-${W}x${H}`;
  const tira = async arq => { const r = await cdp('Page.captureScreenshot', { format: 'jpeg', quality: 72 }); writeFileSync(arq, Buffer.from(r.result.data, 'base64')); };
  if (inteira) {
    const total = (await cdp('Runtime.evaluate', { expression: 'document.documentElement.scrollHeight', returnByValue: true })).result.result.value;
    let k = 0; for (let y = 0; y < total; y += Math.round(H * .9), k++) {
      await cdp('Runtime.evaluate', { expression: `scrollTo(0,${y})` }); await sleep(900);
      await tira(`${nome}-${String(k).padStart(2, '0')}.jpg`); }
    console.log(`${nome}-*.jpg: ${k} telas`);
  } else await tira(nome + '.jpg');
  const largura = (await cdp('Runtime.evaluate', { expression: 'document.documentElement.scrollWidth', returnByValue: true })).result.result.value;
  console.log(nome, largura > W ? `⚠ rolagem lateral: conteúdo com ${largura}px` : 'ok', `(${((Date.now() - t0) / 1000).toFixed(1)}s)`);
}
console.log(erros.length ? 'ERROS DE SCRIPT:\n - ' + [...new Set(erros)].join('\n - ') : 'sem erros de script');
limpa(); await sleep(900); process.exit(0);
