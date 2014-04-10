function mostrarPedidos() {
    main.style.display = "none";
    inventory.style.display = "inline-block";
    consulta.style.display = "none";
}

function mostrarConsultas() {
    main.style.display = "none";
    consulta.style.display = "inline-block";
    inventory.style.display = "none";
}

var firstCheck = false;

function admSelectCheck(nameSelect) {
    if (nameSelect) {
        admOptionValue = nameSelect.value;
        if (admOptionValue != "null") {
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
            document.getElementById("password").value = "";
            document.getElementById("enviar").disabled = true;
            firstCheck = false;
        }
    }
}

function cambioFecha(nameSelect) {
    if (nameSelect) {
        admOptionValue = nameSelect.value;
        if (admOptionValue != "0") {
            futuro.style.display = "inline-block";
            fecha.style.display = "none";
        };
    }
}

function enable(nameSelect) {
    admOptionValue = nameSelect.value;
    if ((admOptionValue != 0) && (firstCheck == true)) {
        document.getElementById("enviar").disabled = false;
    } else {
        document.getElementById("enviar").disabled = true;
    };
}

function get_bebidas() {
    request = new XMLHttpRequest();
    request.open('GET', '/api/producto/', true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            data = JSON.parse(request.responseText);
            data = data['objects'];
            var largo_de_lista = data.length;
            ul = document.getElementById('lista');
            for (var i = 0; i < largo_de_lista; ++i) {
                var nuevo_item = document.createElement('li');
                if (data[i]['cant'] != 0) {
                    nuevo_item.innerHTML = data[i]['nombre'] + ' <b>x' + data[i]['cant'] + '</b>';
                } else {
                    nuevo_item.innerHTML = data[i]['nombre'] + ' <span class="err">No hay</span>';
                };
                ul.appendChild(nuevo_item);
            }
        } else {
            return console.log('Error');
        }
    };

    request.onerror = function() {
        return alert('Error');
    };

    request.send();
}

function refrescar_bebidas() {
    var ul = document.getElementById('lista');
    ul.innerHTML = '';
    get_bebidas();
}

document.addEventListener('DOMContentLoaded', function() {
    get_bebidas();
    var refrescar = setInterval(function() {
        refrescar_bebidas()
    }, 60000);
});