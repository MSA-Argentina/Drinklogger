function mostrarPedidos() {
    main.style.display = "none";
    inventory.style.display = "inline-block";
    consulta.style.display = "none";
    $("#checklogin").hide();
    $('#password').val('');
    $('#personas option[value="0"]').prop('selected', true);
    $('#add_err').removeClass('uk-alert-warning uk-alert uk-alert-success');
    $('#add_err').html('');

    cargar_bebidas();
}

function mostrarConsultas() {
    main.style.display = "none";
    consulta.style.display = "inline-block";
    inventory.style.display = "none";
}

function aStock() {
    main.style.display = "inline-block";
    consulta.style.display = "none";
    inventory.style.display = "none";
}

var firstCheck = false;

function admSelectCheck(nameSelect) {
    if (nameSelect) {
        admOptionValue = nameSelect.value;
        if (admOptionValue != "null") {
            cantidad.style.display = "inline-block";
            $("#persona").show();
            $("#pass").show();
            $("#checklogin").show();
            firstCheck = true;
        } else {
            cantidad.style.display = "none";
            $("#persona").hide();
            $("#pass").hide();
            document.getElementById("personas").selectedIndex = 0;
            document.getElementById("personas").value = 0;
            document.getElementById("password").value = "";
            $("#checklogin").hide();
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
        $("#checklogin").prop('disabled', false);
    } else {
        $("#checklogin").prop('disabled', true);
    };
}

function get_bebidas() {
    request = new XMLHttpRequest();
    request.open('GET', '/api/producto/?ordering=id', true);

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
            setTimeout(function() {
                get_bebidas();
            }, 2000);
            return console.log('Error de conexión. Reintentando...');
        }
    };

    request.onerror = function() {
        setTimeout(function() {
            get_bebidas();
        }, 2000);
        return console.log('Error de conexión. Reintentando...');
    };

    request.send();
}

function refrescar_bebidas() {
    var ul = document.getElementById('lista');
    ul.innerHTML = '';
    get_bebidas();
}

function cargar_bebidas() {
    request = new XMLHttpRequest();
    request.open('GET', '/api/producto/?ordering=id', true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            data = JSON.parse(request.responseText);
            data = data['objects'];
            var largo_de_lista = data.length;
            opciones = document.getElementById('productos');
            opciones.innerHTML = '';
            // Elemento nulo
            nulo = document.createElement('option');
            nulo.value = "null";
            nulo.innerHTML = "------------";
            opciones.appendChild(nulo);
            for (var i = 0; i < largo_de_lista; ++i) {
                var nuevo_item = document.createElement('option');
                if (data[i]['cant'] != 0) {
                    nuevo_item.value = data[i]['id'];
                    nuevo_item.innerHTML = data[i]['nombre'];
                } else {
                    nuevo_item.disabled = true;
                    nuevo_item.innerHTML = data[i]['nombre'];
                };
                opciones.appendChild(nuevo_item);
            }
        } else {
            return console.log('Error');
        }
    };

    request.onerror = function() {
        setTimeout(function() {
            cargar_bebidas();
        }, 2000);
        return console.log('Error de conexión. Reintentando...');
    };

    request.send();
}

function get_Detalle(usuario, pasado, futuro) {

    var consulta_usuario = 'consulta-'.concat(usuario.replace(/\s/g, '-'));
    var detalle = document.getElementById(consulta_usuario);
    var cerrar_detalle = document.getElementById('cerrar-consulta-'.concat(usuario.replace(/\s/g, '-')));
    detalle.style.display = 'none';
    cerrar_detalle.style.display = 'inline-block';

    var url = '/consulta/'.concat(usuario).concat('/');
    var url = url.concat(pasado).concat('-a-');
    var url = url.concat(futuro).concat('/');

    request = new XMLHttpRequest();
    request.open('GET', url, true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            data = JSON.parse(request.responseText);
            var td_usuario = 'usuario-'.concat(usuario.replace(/\s/g, '-'));
            detalle = document.getElementById(td_usuario).children[0];
            var lista_detalle = document.createElement('ul');
            detalle.innerHTML = '';
            lista_detalle.innerHTML = '';
            for (var i = data["cantidad"].length - 1; i >= 0; i--) {
                var detalle_elemento = document.createElement('li');
                detalle_elemento.innerHTML = ''.concat(data["fecha"][i]).concat(' - ').concat(data["producto"][i]).concat(' x').concat(data["cantidad"][i]).concat('($').concat(data["precio"][i]).concat(')');
                lista_detalle.appendChild(detalle_elemento);
            };
            detalle.appendChild(lista_detalle);

        } else {
            return console.log('Error');
        }
    };

    request.onerror = function() {
        setTimeout(function() {
            get_Detalle();
        }, 2000);
        return console.log('Error de conexión. Reintentando...');
    };

    request.send();
}

function cerrar_Detalle(padre) {
    var padre = document.getElementById(padre);
    var padre_id = padre.id.replace('usuario-', '');
    padre_link = document.getElementById('cerrar-consulta-'.concat(padre_id));
    var padre_detalle_link = document.getElementById('consulta-'.concat(padre_id));
    padre_link.style.display = 'none';
    padre_detalle_link.style.display = 'inline-block';
    hijo = padre.children[0];
    hijo.innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname == '/') {
        get_bebidas();
        var refrescar_stock = setInterval(function() {
            refrescar_bebidas()
        }, 30000);
        var refrescar_pedido = setInterval(function() {
            cargar_bebidas()
        }, 300000);
    };
});

$(document).ready(function() {
    $("#checklogin").click(function() {
        personas = $("#personas").val();
        pass = $("#password").val();
        pass = $.md5(pass);
        producto = $("#productos").val();
        cant = $("#cantidad").val();
        if (pass != '' && personas > 0 && producto > 0) {
            $.ajax({
                type: "POST",
                encoding: "UTF-8",
                url: "checklogin?" + "personas=" + personas + "&pass=" + encodeURIComponent(pass) + "&productos=" + producto + "&cantidad=" + cant,
                success: function(html) {
                    //alert(JSON.stringify(html));
                    var obj = jQuery.parseJSON(JSON.stringify(html));
                    $('#add_err').removeClass('uk-alert-warning').addClass(obj.MSGUK);
                    $('#add_err').html(obj.MSG);
                    $('#password').val('');
                    $('#productos').empty();
                    cargar_bebidas();
                    $('#personas option[value="0"]').prop('selected', true);
                    $('#add_err').fadeOut(5000);
                    if (obj.estado == 200) {
                        $('#inventory').fadeOut(5000);
                        $('#main').fadeIn(5000);
                    }
                },
                beforeSend: function() {
                    $("#add_err").html("Cargando Datos...");
                }
            });
        } else {
            $('#add_err').html('Completar todos los campos para realizar el pedido');
            $('#add_err').addClass('uk-alert uk-alert-warning');
            $('#add_err').hide().fadeIn().delay(3000).fadeOut('slow');
        }
        return false;
    });
});