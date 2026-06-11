document.addEventListener("DOMContentLoaded", () => {
    var ipt_search = document.getElementById("input_search");

    ipt_search.addEventListener("keydown", (e) => {
        if (e.code === "Enter") {
            let url = `/api/buyer/${ipt_search.value}`;
            axios.get(url).then(result => {
                var buyers = result.data;
                var table = document.getElementById("mgt_body");
                table.innerHTML = "";

                for (var item of buyers) {
                    var row = table.insertRow();
                    row.insertCell(0).innerHTML = item.nome;
                    row.insertCell(1).innerHTML = item.whatsapp;
                    row.insertCell(2).innerHTML = item.tipo || "";
                    row.insertCell(3).innerHTML = item.quantidade || "";
                    row.insertCell(4).innerHTML = item.ativo ? "Sim" : "Não";
                    row.insertCell(5).innerHTML = `<a href='/buyer/edit/${item.id}'><img class='edit' src='/static/edit.png'></a>`;
                }
            }).catch(error => console.log(error));
        }
    });
});
