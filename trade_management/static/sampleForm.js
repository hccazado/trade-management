document.addEventListener('DOMContentLoaded', () => {
    const el = document.getElementById('client');
    if (el) new Choices(el, { searchEnabled: true, itemSelectText: '', shouldSort: false });
});
