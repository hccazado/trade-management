document.addEventListener("DOMContentLoaded", () => {
    var ipt_search = document.getElementById("input_search");

    ipt_search.addEventListener('keydown', (e) => {
        if (e.code == "Enter") {
            let query = ipt_search.value.trim();
            if (!query) {
                // If query is empty, reload page to get full list
                window.location.reload();
                return;
            }
            
            let url = `/api/sample/${query}`;
            axios.get(url).then(result => {
                var samples = result.data;
                var table = document.getElementById("mgt_body");
                table.innerHTML = "";

                for (var item of samples) {
                    var row = table.insertRow();
    
                    var cell_client = row.insertCell(0);
                    cell_client.innerHTML = item.client_name || '';
    
                    var cell_date = row.insertCell(1);
                    cell_date.innerHTML = item.data || '';
    
                    var cell_17_8 = row.insertCell(2);
                    cell_17_8.innerHTML = item['17/8'] || '';
    
                    var cell_13 = row.insertCell(3);
                    cell_13.innerHTML = item['13'] || '';

                    var cell_10 = row.insertCell(4);
                    cell_10.innerHTML = item['10'] || '';

                    var cell_mk = row.insertCell(5);
                    cell_mk.innerHTML = item['Mk'] || '';

                    var cell_fd = row.insertCell(6);
                    cell_fd.innerHTML = item['FD'] || '';

                    var cell_cata = row.insertCell(7);
                    cell_cata.innerHTML = item['Cata'] || '';

                    var cell_pva = row.insertCell(8);
                    cell_pva.innerHTML = item['PVA'] || '';

                    var cell_broca = row.insertCell(9);
                    cell_broca.innerHTML = item['Broca'] || '';

                    var cell_edit = row.insertCell(10);
                    cell_edit.innerHTML = `<a href='/sample/edit/${item.id}'><img class='edit' src='/static/edit.png'></a>`;
                }
            })
            .catch(error => console.log(error)); 
        }
    });
});
