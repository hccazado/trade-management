document.addEventListener('DOMContentLoaded', ()=>{
    
    console.log("cep.js - document loaded!");

    cep = document.getElementById("cep");

    cep.addEventListener("keyup", ()=>{
        
        cep_value = cep.value;
        
        if(cep_value.length == 8){
            
            get_address(cep_value);

        }
    })
})

function get_address(cep){

    url = `https://viacep.com.br/ws/${cep}/json/`;

    call = axios.get(url).then(result=>{
        endereco = document.getElementById("endereco").value = result.data.logradouro;
        
        bairro = document.getElementById("bairro").value = result.data.bairro;
        
        cidade = document.getElementById("cidade").value = result.data.localidade;
        
        uf = document.getElementById("uf").value = result.data.uf;
        
        //complemento = document.getElementById("complemento").value = result.data.complemento;

    })
    .catch(error => {
        console.log("Something went wrong consulting viacep: "+error);
    })
}

//URL: viacep.com.br/ws/38742038/json/