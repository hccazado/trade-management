document.addEventListener('DOMContentLoaded', () => {
    const opts = { searchEnabled: true, itemSelectText: '', shouldSort: false };
    ['vendedor', 'comprador', 'retirada', 'descarga'].forEach(id => {
        const el = document.getElementById(id);
        if (el) new Choices(el, opts);
    });
});
