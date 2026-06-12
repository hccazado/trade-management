document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input_search");
    const rows = document.querySelectorAll("#mgt_body tr");
    input.addEventListener("input", () => {
        const q = input.value.trim().toLowerCase();
        rows.forEach(row => {
            if (!q) { row.style.display = ""; return; }
            const data = JSON.parse(row.dataset.sample || "{}");
            const haystack = [data.num_amostra||"", data.type||"", data.client_name||""].join(" ").toLowerCase();
            row.style.display = haystack.includes(q) ? "" : "none";
        });
    });
});
