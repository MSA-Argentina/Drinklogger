function mostrarPedidos () {
    main.style.display = "none";
    inventory.style.display = "inline-block";
    consulta.style.display = "none";
}

function mostrarConsultas () {
    main.style.display = "none";
    consulta.style.display = "inline-block";
    inventory.style.display = "none";
}

var firstCheck = false; // Work in Progress

function admSelectCheck(nameSelect)
{
    if(nameSelect){
        admOptionValue = nameSelect.value;
        if(admOptionValue != "null"){
            cantidad.style.display = "inline-block";
            persona.style.display = "inline-block";
            };
        }
        else {
            persona.style.display = "none";
        }
}

function cambioFecha(nameSelect)
{
    if(nameSelect){
        admOptionValue = nameSelect.value;
        if(admOptionValue != "0"){
            futuro.style.display = "inline-block";
            fecha.style.display = "none";
            };
        }
}

function enable (nameSelect) {
    admOptionValue = nameSelect.value;
    if (admOptionValue != 0) {
        document.getElementById("enviar").disabled = false;
    } else {
        document.getElementById("enviar").disabled = true;
    };
}