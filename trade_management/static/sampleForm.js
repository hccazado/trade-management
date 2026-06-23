// ── Client autocomplete ──────────────────────────────────────────────────────
(function () {
    const formData   = JSON.parse(document.getElementById('sample-form-data').textContent);
    const ALL_CLIENTS = formData.clients;

    const searchEl  = document.getElementById('client_search');
    const hiddenEl  = document.getElementById('client');
    const dropdown  = document.getElementById('client_dropdown');
    let activeIndex = -1;

    function renderList(items) {
        dropdown.innerHTML = '';
        activeIndex = -1;
        if (!items.length) { dropdown.classList.add('d-none'); return; }
        items.forEach(c => {
            const li = document.createElement('li');
            li.className    = 'list-group-item list-group-item-action py-1 px-2';
            li.style.cursor = 'pointer';
            li.textContent  = c.nome;
            li.dataset.id   = c.id;
            li.addEventListener('mousedown', e => {
                e.preventDefault();
                selectClient(c);
            });
            dropdown.appendChild(li);
        });
        dropdown.classList.remove('d-none');
    }

    function selectClient(c) {
        searchEl.value = c.id === '' ? '' : c.nome;
        hiddenEl.value = c.id;
        dropdown.classList.add('d-none');
        activeIndex = -1;
    }

    function filter(q) {
        const lower = q.toLowerCase().trim();
        if (!lower) return ALL_CLIENTS;
        return ALL_CLIENTS.filter(c => c.nome.toLowerCase().includes(lower));
    }

    function highlight(delta) {
        const items = dropdown.querySelectorAll('li');
        if (!items.length) return;
        items[activeIndex]?.classList.remove('active');
        activeIndex = Math.max(0, Math.min(activeIndex + delta, items.length - 1));
        items[activeIndex].classList.add('active');
        items[activeIndex].scrollIntoView({ block: 'nearest' });
    }

    searchEl.addEventListener('input', () => {
        hiddenEl.value = '';
        renderList(filter(searchEl.value));
    });

    searchEl.addEventListener('focus', () => renderList(filter(searchEl.value)));

    searchEl.addEventListener('keydown', e => {
        if (e.key === 'ArrowDown')       { e.preventDefault(); highlight(1); }
        else if (e.key === 'ArrowUp')    { e.preventDefault(); highlight(-1); }
        else if (e.key === 'Enter') {
            const active = dropdown.querySelector('li.active');
            if (active) { e.preventDefault(); selectClient({ id: active.dataset.id, nome: active.textContent }); }
        }
        else if (e.key === 'Escape')     { dropdown.classList.add('d-none'); }
    });

    document.addEventListener('click', e => {
        if (!searchEl.contains(e.target) && !dropdown.contains(e.target))
            dropdown.classList.add('d-none');
    });
})();
