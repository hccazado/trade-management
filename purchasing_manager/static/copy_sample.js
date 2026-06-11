function buildSampleText(d) {
    const lines = [];

    if (d.num_amostra) lines.push(`Amostra: ${d.num_amostra}`);
    if (d.client_name)  lines.push(`Cliente: ${d.client_name}`);
    if (d.type)         lines.push(`Tipo: ${capitalize(d.type)}`);
    if (d.data)         lines.push(`Data: ${d.data}`);

    const peneiras = [];
    for (const key of ['17/8','13','10','Mk','FD','Cata','PVA','Broca']) {
        const v = d[key];
        if (v !== undefined && v !== null && v !== '') peneiras.push(`${key}: ${v}%`);
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

function capitalize(s) {
    return s ? s.charAt(0).toUpperCase() + s.slice(1) : '';
}

function copySample(data, btn) {
    const text = buildSampleText(data);
    const finish = () => {
        const original = btn.textContent;
        btn.textContent = '✓ Copiado';
        btn.disabled = true;
        setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 2000);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(finish).catch(() => fallbackCopy(text, btn));
    } else {
        fallbackCopy(text, btn);
    }
}

function fallbackCopy(text, btn) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
        document.execCommand('copy');
        const original = btn.textContent;
        btn.textContent = '✓ Copiado';
        btn.disabled = true;
        setTimeout(() => { btn.textContent = original; btn.disabled = false; }, 2000);
    } catch (e) {
        alert('Não foi possível copiar. Tente novamente.');
    }
    document.body.removeChild(ta);
}

// ── Table rows ──────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-sample]').forEach(row => {
        const btn = row.querySelector('.btn-copy');
        if (!btn) return;
        btn.addEventListener('click', () => {
            const data = JSON.parse(row.dataset.sample);
            copySample(data, btn);
        });
    });

    // ── Edit form ────────────────────────────────────────────────────────────
    const formCopyBtn = document.getElementById('btn-copy-form');
    if (formCopyBtn) {
        formCopyBtn.addEventListener('click', () => {
            const g = id => (document.getElementById(id) || {}).value || '';
            const data = {
                num_amostra: g('num_amostra'),
                client_name: document.getElementById('client')?.selectedOptions[0]?.text || '',
                type:        g('type'),
                data:        g('data'),
                '17/8': g('17/8'), '13': g('13'), '10': g('10'),
                Mk: g('Mk'), FD: g('FD'), Cata: g('Cata'), PVA: g('PVA'), Broca: g('Broca'),
                Duro: g('Duro'), Riado: g('Riado'), Rio: g('Rio'),
                Fermentado: g('Fermentado'), Sujo: g('Sujo'),
                quantidade: g('quantidade'),
                obs: g('obs'),
            };
            copySample(data, formCopyBtn);
        });
    }
});
