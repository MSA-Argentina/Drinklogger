function mostrar () {
    main.style.display = "none";
    inventory.style.display = "inline-block";
}

var firstCheck = false; // Work in Progress

function admSelectCheck(nameSelect)
{
    if(nameSelect){
        admOptionValue = nameSelect.value;
        if(admOptionValue != "null"){
            quantity.style.display = "inline-block";
            };
        }
        else {
            quantity.style.display = "none";
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