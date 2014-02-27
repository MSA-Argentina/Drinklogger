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

var firstCheck = false;

function admSelectCheck(nameSelect)
{
    if(nameSelect){
        admOptionValue = nameSelect.value;
        if(admOptionValue != "null"){
            cantidad.style.display = "inline-block";
            persona.style.display = "inline-block";
            pass.style.display = "inline-block";
            firstCheck = true;
        } else {
            cantidad.style.display = "none";
            persona.style.display = "none";
            pass.style.display = "none";
            document.getElementById("personas").selectedIndex = 0;
            document.getElementById("personas").value = 0;
            document.getElementById("enviar").disabled = true;
            firstCheck = false;
        }
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
    if ((admOptionValue != 0) && (firstCheck == true)) {
        document.getElementById("enviar").disabled = false;
    } else {
        document.getElementById("enviar").disabled = true;
    };
}