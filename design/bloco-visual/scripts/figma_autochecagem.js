// Autochecagem de montagem no Figma: usada pela /bloco-visual (e por qualquer skill que componha peças no Figma).
// Colar esta função no FIM do script do use_figma que monta ou corrige, e devolver o resultado junto com os IDs:
//   const chk = await autochecagem(frame, { familias: ['Inter'], larguraMax: 2160, enfases: [...], copy: [...] });
// Não gasta chamada extra: roda dentro da mesma chamada da montagem.
// Cada problema sai como [tipo, nodeId, detalhe]. ok:false → corrigir na mesma rodada, antes do print.
//
// opções:
//   familias   — famílias do bloco do cliente; qualquer outra = substituição silenciosa
//   larguraMax — limite dos filhos diretos do frame (bloco: 2160)
//   enfases    — [{ nodeId, trecho, styleId }] confere que só o trecho tem o estilo de ênfase
//   copy       — [{ nodeId, texto }] confere a copy verbatim, caractere por caractere
async function autochecagem(root, o = {}) {
  const P = [];
  const box = n => n.absoluteBoundingBox;
  const vis = n => Array.isArray(n.fills) ? n.fills.filter(f => f.visible !== false && (f.opacity ?? 1) > 0) : [];
  const branco = p => p && p.type === 'SOLID' && (p.opacity ?? 1) > 0.99 && p.color.r > 0.99 && p.color.g > 0.99 && p.color.b > 0.99;
  const nodes = [root, ...root.findAll(() => true)];
  for (const n of nodes) {
    if (n.type === 'TEXT') {
      const ch = n.characters.trim();
      if (n.hasMissingFont) P.push(['fonte ausente', n.id, n.name]);
      if (o.familias) for (const s of n.getStyledTextSegments(['fontName']))
        if (!o.familias.includes(s.fontName.family)) P.push(['família fora do bloco', n.id, s.fontName.family + ' ' + s.fontName.style]);
      if (n.textAutoResize === 'NONE' || n.textAutoResize === 'TRUNCATE' || n.textTruncation === 'ENDING')
        P.push(['texto pode cortar (altura fixa ou truncado)', n.id, ch.slice(0, 40)]);
      if (!ch || ['Title', 'Heading', 'Button', 'Text', 'Label'].includes(ch)) P.push(['texto vazio ou placeholder', n.id, ch]);
      if (n.width < 2) P.push(['texto com largura ~0', n.id, ch.slice(0, 40)]);
    }
    const pai = n.parent;
    if (n !== root && pai && pai.type !== 'PAGE' && box(n) && box(pai)) {
      const b = box(n), pb = box(pai);
      if (b.x < pb.x - 1 || b.y < pb.y - 1 || b.x + b.width > pb.x + pb.width + 1 || b.y + b.height > pb.y + pb.height + 1)
        P.push(['passa da moldura do pai', n.id, n.name + ' em ' + pai.name]);
    }
    for (const f of vis(n)) if (f.type === 'IMAGE' && !f.imageHash) P.push(['imagem sem arquivo', n.id, n.name]);
    if (['FRAME', 'COMPONENT', 'INSTANCE'].includes(n.type) && n !== root) {
      const f = vis(n);
      if (f.length && branco(f[f.length - 1])) {
        let a = n.parent;
        while (a && a.type !== 'PAGE' && !vis(a).length) a = a.parent;
        const af = a && a.type !== 'PAGE' ? vis(a) : [];
        const topo = af[af.length - 1];
        if (topo && !branco(topo)) P.push(['moldura branca sobre cor ou foto', n.id, n.name]);
      }
    }
  }
  if (o.larguraMax) for (const c of root.children)
    if (c.width > o.larguraMax + 0.5) P.push(['largura acima do limite', c.id, c.name + ' ' + Math.round(c.width)]);
  for (const e of o.enfases || []) {
    const t = await figma.getNodeByIdAsync(e.nodeId);
    const i = t ? t.characters.indexOf(e.trecho) : -1;
    if (i < 0) { P.push(['ênfase: trecho não está no texto', e.nodeId, e.trecho]); continue; }
    const j = i + e.trecho.length;
    if (t.getRangeFillStyleId(i, j) !== e.styleId) P.push(['ênfase com estilo errado ou parcial', e.nodeId, e.trecho]);
    if (i > 0 && t.getRangeFillStyleId(i - 1, i) === e.styleId) P.push(['ênfase vazou para antes do trecho', e.nodeId, e.trecho]);
    if (j < t.characters.length && t.getRangeFillStyleId(j, j + 1) === e.styleId) P.push(['ênfase vazou para depois do trecho', e.nodeId, e.trecho]);
  }
  for (const c of o.copy || []) {
    const t = await figma.getNodeByIdAsync(c.nodeId);
    if (!t || t.characters !== c.texto) P.push(['copy diferente da aprovada', c.nodeId, t ? t.characters.slice(0, 60) : 'nó não existe']);
  }
  return { ok: P.length === 0, total: P.length, problemas: P.slice(0, 40), nos: nodes.length };
}
