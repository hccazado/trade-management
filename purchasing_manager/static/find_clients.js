function search(value){
   
}

document.addEventListener("DOMContentLoaded", ()=>{

    var ipt_search = document.getElementById("input_search");

    ipt_search.addEventListener('keydown',(e)=>{

        if(e.code == "Enter"){
            
            let url = `http://127.0.0.1:5000/api/client/${ipt_search.value}`
            var result = axios.get(url).then(result=>{
                var warehouses = result.data;

                var table = document.getElementById("mgt_body");
                
                table.innerHTML = "";

                for (item of warehouses){

                    var row = table.insertRow();
                       
                    var date_0 = row.insertCell(0);
                        
                    date_0.innerHTML = item.id;
    
                    var date_1 = row.insertCell(1);
                        
                    date_1.innerHTML = item.nome;
    
                    var date_2 = row.insertCell(2);
                        
                    date_2.innerHTML = item.cnpj;
    
                    var date_3 = row.insertCell(3);
                        
                    date_3.innerHTML = `${item.cidade} / ${item.uf}`;
    
                    var date_4 = row.insertCell(4);
                    
                    date_4.innerHTML = `<a href='/warehouse/edit/${item.id}'><img class='edit' src='/static/edit.png'></a>`;
    
                }
            })
            .catch (error =>console.log(error)); 
        }
    })
})

