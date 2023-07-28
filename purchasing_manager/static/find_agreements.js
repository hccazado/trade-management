document.addEventListener("DOMContentLoaded", ()=>{

    var ipt_search = document.getElementById("input_search");

    ipt_search.addEventListener('keydown',(e)=>{
        if (e.code == "Enter") {
            let url = `http://127.0.0.1:5000/api/agreement/${ipt_search.value}`;
            var result = axios.get(url).then(result => {
                var agreements = result.data;

                var table = document.getElementById("mgt_body");

                table.innerHTML = "";

                for (item of agreements) {

                    var row = table.insertRow();

                    var date_0 = row.insertCell(0);

                    date_0.innerHTML = item.data;

                    var date_1 = row.insertCell(1);

                    date_1.innerHTML = item.num_fechamento;

                    var date_2 = row.insertCell(2);

                    date_2.innerHTML = item.rc;

                    var date_3 = row.insertCell(3);

                    date_3.innerHTML = item.vendedor;

                    var date_4 = row.insertCell(4);

                    date_4.innerHTML = item.comprador;

                    var date_5 = row.insertCell(5);

                    date_5.innerHTML = item.quantidade;

                    var date_6 = row.insertCell(6);

                    date_6.innerHTML = `<a href='/agreement/edit/${item.id}'><img class='edit' src='/static/edit.png'></a>`
                        + `<a href='/agreement/print/${item.id}'><img class='edit' src='/static/print.png'></a>`;

                }
            })
            .catch(error => console.log(error));
        }
    });
})

        