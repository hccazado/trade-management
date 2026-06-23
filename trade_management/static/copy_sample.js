function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
}

// ── Plain text ───────────────────────────────────────────────────────────────

function buildSampleText(d) {
    const lines = [];
    if (d.num_amostra) lines.push(`Amostra: ${d.num_amostra}`);
    if (d.type)        lines.push(`Tipo: ${capitalize(d.type)}`);
    if (d.data)        lines.push(`Data: ${d.data}`);

    const peneiras = [];
    for (const k of ['17/8','16','13','Fd13','Cata','Broca','Imp','10','FD','PVA','Mk']) {
        const v = d[k];
        if (v !== undefined && v !== null && v !== '') peneiras.push(`${k}: ${v}%`);
    }
    if (peneiras.length) lines.push(`Peneiras: ${peneiras.join(' | ')}`);

    const bebida = [];
    for (const b of ['Duro','Riado','Rio','Fermentado','Sujo']) {
        const v = parseInt(d[b] || 0);
        if (v > 0) bebida.push(`${b}: ${v} copo${v > 1 ? 's' : ''}`);
    }
    if (bebida.length) lines.push(`Bebida: ${bebida.join(' | ')}`);

    if (d.quantidade) lines.push(`Quantidade: ${d.quantidade} sacas`);
    if (d.obs)        lines.push(`OBS: ${d.obs}`);

    return lines.join('\n');
}

// ── Slip image ───────────────────────────────────────────────────────────────

function wrapText(ctx, text, maxWidth) {
    const words = String(text).split(' ');
    const lines = [];
    let line = '';
    for (const word of words) {
        const test = line ? line + ' ' + word : word;
        if (ctx.measureText(test).width > maxWidth && line) {
            lines.push(line);
            line = word;
        } else {
            line = test;
        }
    }
    if (line) lines.push(line);
    return lines;
}

function generateSlipCanvas(data) {
    const scale    = 2;
    const W        = 340;
    const BORDER   = 10;
    const LABEL_W  = 72;
    const ROW_H    = 26;
    const LINE_H   = 13;
    const HEADER_H = 62;
    const divX     = BORDER + LABEL_W;
    const valueMaxW = W - divX - 10 - BORDER;

    const tmp = document.createElement('canvas').getContext('2d');
    tmp.font  = 'bold 10px Arial, sans-serif';

    function makeRow(label, value) {
        if (value === '' || value === undefined || value === null) return null;
        const str   = String(value);
        const lines = wrapText(tmp, str, valueMaxW);
        const h     = Math.max(ROW_H, lines.length * LINE_H + 8);
        return { label, str, lines, h };
    }

    const PENEIRAS = ['17/8','16','13','Fd13','Cata','Broca','Imp','10','FD','PVA','Mk'];
    const penRows  = PENEIRAS
        .map(k => makeRow(k, data[k] !== '' && data[k] != null ? `${data[k]}%` : ''))
        .filter(Boolean);

    const bebidaItems = ['Duro','Riado','Rio','Fermentado','Sujo']
        .filter(k => parseInt(data[k] || 0) > 0)
        .map(k => `${data[k]}c ${k}`);

    const mainRows = [
        makeRow('Sacas',   data.quantidade),
        ...penRows,
        bebidaItems.length ? makeRow('Bebida', bebidaItems.join('  ')) : null,
    ].filter(Boolean);

    const bottomLeftRows = [
        makeRow('Data', data.data),
        makeRow('OBS',  data.obs),
    ].filter(Boolean);

    const tipoStr  = data.type ? capitalize(data.type) : '';
    const mainH    = mainRows.reduce((s, r) => s + r.h, 0);
    const bottomH  = Math.max(
        bottomLeftRows.reduce((s, r) => s + r.h, 0),
        tipoStr ? ROW_H * 2 : 0,
        ROW_H
    );
    const H = HEADER_H + mainH + bottomH + BORDER;

    const canvas  = document.createElement('canvas');
    canvas.width  = W * scale;
    canvas.height = H * scale;
    const ctx     = canvas.getContext('2d');
    ctx.scale(scale, scale);

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle = '#111';
    ctx.lineWidth   = 1.5;
    ctx.strokeRect(BORDER, BORDER, W - BORDER * 2, H - BORDER * 2);

    // Header
    ctx.fillStyle = '#111';
    ctx.textAlign = 'left';
    ctx.font      = 'bold 14px Georgia, serif';
    ctx.fillText('Caza do Café', BORDER + 8, BORDER + 20);
    ctx.font      = '9px Arial, sans-serif';
    ctx.fillStyle = '#444';
    ctx.fillText('Ficha de Amostra', BORDER + 8, BORDER + 34);
    if (data.num_amostra) {
        ctx.textAlign = 'right';
        ctx.font      = 'bold 11px Arial, sans-serif';
        ctx.fillStyle = '#111';
        ctx.fillText(`Nº ${data.num_amostra}`, W - BORDER - 6, BORDER + 20);
    }

    ctx.beginPath();
    ctx.moveTo(BORDER, HEADER_H);
    ctx.lineTo(W - BORDER, HEADER_H);
    ctx.lineWidth   = 1;
    ctx.strokeStyle = '#111';
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(divX, HEADER_H);
    ctx.lineTo(divX, H - BORDER);
    ctx.lineWidth   = 0.8;
    ctx.strokeStyle = '#111';
    ctx.stroke();

    // Main rows
    let curY = HEADER_H;
    for (const row of mainRows) {
        const midY  = curY + row.h / 2;
        ctx.fillStyle  = '#444';
        ctx.font       = '9px Arial, sans-serif';
        ctx.textAlign  = 'right';
        ctx.fillText(row.label + ':', divX - 5, midY + 4);
        ctx.fillStyle  = '#000';
        ctx.font       = 'bold 10px Arial, sans-serif';
        ctx.textAlign  = 'left';
        const startY   = curY + (row.h - row.lines.length * LINE_H) / 2 + LINE_H;
        row.lines.forEach((ln, i) => ctx.fillText(ln, divX + 6, startY + i * LINE_H, valueMaxW));
        ctx.beginPath();
        ctx.moveTo(BORDER, curY + row.h);
        ctx.lineTo(W - BORDER, curY + row.h);
        ctx.lineWidth   = 0.5;
        ctx.strokeStyle = '#999';
        ctx.stroke();
        curY += row.h;
    }

    // Bottom split section
    const splitX  = BORDER + Math.floor((W - BORDER * 2) * 0.55);
    const bottomY = curY;

    ctx.beginPath();
    ctx.moveTo(splitX, bottomY);
    ctx.lineTo(splitX, H - BORDER);
    ctx.lineWidth   = 0.8;
    ctx.strokeStyle = '#111';
    ctx.stroke();

    let leftY = bottomY;
    for (const row of bottomLeftRows) {
        const midY   = leftY + row.h / 2;
        const maxW   = splitX - divX - 10;
        ctx.fillStyle  = '#444';
        ctx.font       = '9px Arial, sans-serif';
        ctx.textAlign  = 'right';
        ctx.fillText(row.label + ':', divX - 5, midY + 4);
        ctx.fillStyle  = '#000';
        ctx.font       = 'bold 10px Arial, sans-serif';
        ctx.textAlign  = 'left';
        const startY   = leftY + (row.h - row.lines.length * LINE_H) / 2 + LINE_H;
        row.lines.forEach((ln, i) => ctx.fillText(ln, divX + 6, startY + i * LINE_H, maxW));
        ctx.beginPath();
        ctx.moveTo(BORDER, leftY + row.h);
        ctx.lineTo(splitX, leftY + row.h);
        ctx.lineWidth   = 0.5;
        ctx.strokeStyle = '#999';
        ctx.stroke();
        leftY += row.h;
    }

    if (tipoStr) {
        const boxMidY = bottomY + bottomH / 2;
        ctx.fillStyle  = '#444';
        ctx.font       = '9px Arial, sans-serif';
        ctx.textAlign  = 'center';
        ctx.fillText('Tipo', (splitX + W - BORDER) / 2, boxMidY - 4);
        ctx.fillStyle  = '#000';
        ctx.font       = 'bold 12px Arial, sans-serif';
        ctx.fillText(tipoStr, (splitX + W - BORDER) / 2, boxMidY + 10);
    }

    return canvas;
}

// ── Copy helpers ─────────────────────────────────────────────────────────────

function finish(btn) {
    const icon = btn.querySelector('.material-symbols-outlined');
    if (icon) icon.textContent = 'check';
    btn.disabled = true;
    setTimeout(() => {
        if (icon) icon.textContent = 'content_copy';
        btn.disabled = false;
    }, 2000);
}

function copyText(text, btn) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => finish(btn)).catch(() => fallbackCopyText(text, btn));
    } else {
        fallbackCopyText(text, btn);
    }
}

function fallbackCopyText(text, btn) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { document.execCommand('copy'); finish(btn); }
    catch { alert('Não foi possível copiar. Tente novamente.'); }
    document.body.removeChild(ta);
}

function copyImage(canvas, btn) {
    canvas.toBlob(async blob => {
        try {
            await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
            finish(btn);
        } catch {
            const url = URL.createObjectURL(blob);
            const a   = document.createElement('a');
            a.href     = url;
            a.download = `amostra.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            finish(btn);
        }
    }, 'image/png');
}

// ── Modal orchestration ──────────────────────────────────────────────────────

let _pendingData = null;
let _pendingBtn  = null;

function showCopyModal(data, btn) {
    _pendingData = data;
    _pendingBtn  = btn;
    const el = document.getElementById('copyModal');
    (bootstrap.Modal.getInstance(el) || new bootstrap.Modal(el)).show();
}

document.addEventListener('DOMContentLoaded', () => {
    const modal       = document.getElementById('copyModal');
    const btnText     = document.getElementById('copyAsText');
    const btnImage    = document.getElementById('copyAsImage');

    function closeModal() {
        bootstrap.Modal.getInstance(modal)?.hide();
    }

    btnText.addEventListener('click', () => {
        closeModal();
        copyText(buildSampleText(_pendingData), _pendingBtn);
    });

    btnImage.addEventListener('click', () => {
        closeModal();
        copyImage(generateSlipCanvas(_pendingData), _pendingBtn);
    });

    // Table rows
    document.querySelectorAll('[data-sample]').forEach(row => {
        const btn = row.querySelector('.btn-copy');
        if (!btn) return;
        btn.addEventListener('click', () => showCopyModal(JSON.parse(row.dataset.sample), btn));
    });

    // Edit form
    const formCopyBtn = document.getElementById('btn-copy-form');
    if (formCopyBtn) {
        formCopyBtn.addEventListener('click', () => {
            const g = id => (document.getElementById(id) || {}).value || '';
            const data = {
                num_amostra: g('num_amostra'),
                client_name: document.getElementById('client')?.selectedOptions[0]?.text || '',
                type:        g('type'),
                data:        g('data'),
                '17/8': g('17/8'), '16': g('16'), '13': g('13'), '10': g('10'),
                Fd13: g('Fd13'), Mk: g('Mk'), FD: g('FD'), Cata: g('Cata'),
                PVA: g('PVA'), Broca: g('Broca'), Imp: g('Imp'),
                Duro: g('Duro'), Riado: g('Riado'), Rio: g('Rio'),
                Fermentado: g('Fermentado'), Sujo: g('Sujo'),
                quantidade: g('quantidade'),
                obs: g('obs'),
            };
            showCopyModal(data, formCopyBtn);
        });
    }
});
