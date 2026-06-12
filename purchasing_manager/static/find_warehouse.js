document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input_search");
    const rows = document.querySelectorAll("#mgt_body tr");
    input.addEventListener("input", () => {
        const q = input.value.trim().toLowerCase();
        rows.forEach(row => {
            row.style.display = (!q || row.textContent.toLowerCase().includes(q)) ? "" : "none";
        });
    });
});
