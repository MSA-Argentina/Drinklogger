function mostrar () {
    main.style.display = 'none';
    inventory.style.display = 'inline-block';
}

var firstCheck = false; // Work in Progress

function admSelectCheck(nameSelect)
{
    if(nameSelect){
        admOptionValue = nameSelect.value;
        if(admOptionValue != 0){
            quantity.style.display = "";
            quantity.options.length = 0;
            switch (admOptionValue) {
                case "1":
                    for ( i = 1; i <= 5; i += 1 ) {
                        option = document.createElement( 'option' );
                        option.value = option.text = i;
                        quantity.add( option );
                    }
                break;
                case "2":
                    for ( i = 1; i <= 3; i += 1 ) {
                        option = document.createElement( 'option' );
                        option.value = option.text = i;
                        quantity.add( option );
                    }
                break;
                case "3":
                    for ( i = 1; i <= 2; i += 1 ) {
                        option = document.createElement( 'option' );
                        option.value = option.text = i;
                        quantity.add( option );
                    }
                break;
                case "4":
                    for ( i = 1; i <= 1; i += 1 ) {
                        option = document.createElement( 'option' );
                        option.value = option.text = i;
                        quantity.add( option );
                    }
                break;
            }
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