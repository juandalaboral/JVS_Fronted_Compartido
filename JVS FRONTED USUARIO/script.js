/* ========================
   NAVEGACIÓN ENTRE MÓDULOS
   ======================== */

function mostrar(id) {
  document.querySelectorAll(".modulo").forEach(m => m.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  if (id === "eventos") renderCarteleraPublicada();
}

function volverAdministrador() {
  localStorage.setItem("admin_entrar_menu", "true");
  window.location.href = "../JVS FRONTED ADMINISTRADOR/index.html";
}

/* ========================
   LOGIN
   ======================== */

function login() {
  let email = document.getElementById("email").value;
  let pass  = document.getElementById("password").value;
  let error = document.getElementById("error");

  let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (email === "" || pass === "") {
    error.innerText = "Digita tus datos";
    error.style.display = "block";
    return;
  }

  if (!regex.test(email)) {
    error.innerText = "Correo no válido";
    error.style.display = "block";
    return;
  }

  error.style.display = "none";

  document.getElementById("loader").style.display = "flex";

  setTimeout(() => {
    document.getElementById("loader").style.display = "none";
    mostrar("eventos");
  }, 1200);
}

/* ========================
   CONTRASEÑA
   ======================== */

function togglePass() {
  let p = document.getElementById("pass");
  p.type = p.type === "password" ? "text" : "password";
}

/* ========================
   CIUDADES POR PAÍS
   ======================== */

function ciudades() {
  let pais = document.getElementById("pais").value;
  let c    = document.getElementById("ciudad");
  c.innerHTML = "";

  let lista = {
    Colombia:  ["Bogotá", "Medellín", "Cali"],
    México:    ["CDMX", "Guadalajara", "Monterrey"],
    España:    ["Madrid", "Barcelona", "Valencia"],
    Argentina: ["Buenos Aires", "Córdoba"],
    Chile:     ["Santiago", "Valparaiso"]
  };

  lista[pais].forEach(ci => {
    let op  = document.createElement("option");
    op.text = ci;
    c.add(op);
  });
}

ciudades(); // Cargar ciudades al iniciar

/* ========================
   CARTELERA PUBLICADA
   ======================== */

function escaparHTML(valor = "") {
  return String(valor)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function limpiarFecha(fecha = "") {
  return String(fecha).replace(/^\D*(?=\d)/, "").trim();
}

function obtenerJSON(clave) {
  return JSON.parse(localStorage.getItem(clave)) || [];
}

function ocultarEventosBaseEliminados() {
  let eliminados = obtenerJSON("eventos_base_eliminados");

  document.querySelectorAll("[data-event-id]").forEach(tarjeta => {
    tarjeta.style.display = eliminados.includes(tarjeta.dataset.eventId) ? "none" : "";
  });
}

function obtenerCarteleraVigente() {
  let cartelera = obtenerJSON("cartelera_usuario");
  let eventosBooking = obtenerJSON("eventos_publicados");
  let eliminadosBase = obtenerJSON("eventos_base_eliminados");
  let idsBooking = eventosBooking.map(evento => evento.id);

  let vigente = cartelera.filter(evento => {
    if (eliminadosBase.includes(evento.id)) return false;
    if (String(evento.id).startsWith("evento_") && !idsBooking.includes(evento.id)) return false;
    return true;
  });

  if (vigente.length !== cartelera.length) {
    localStorage.setItem("cartelera_usuario", JSON.stringify(vigente));
  }

  return vigente;
}

function renderCarteleraPublicada() {
  let contenedor = document.getElementById("listaEventosUsuario");
  if (!contenedor) return;

  ocultarEventosBaseEliminados();
  contenedor.querySelectorAll(".evento-publicado").forEach(evento => evento.remove());
  let cartelera = obtenerCarteleraVigente();

  cartelera.forEach(evento => {
    let fechaPrincipal = evento.fechas && evento.fechas.length
      ? limpiarFecha(evento.fechas[0])
      : "Por confirmar";

    contenedor.insertAdjacentHTML("beforeend", `
      <div class="evento evento-publicado">
        <img src="${escaparHTML(evento.img)}" alt="${escaparHTML(evento.nombre)}">
        <h3>${escaparHTML(evento.nombre)}</h3>
        <p>Fecha: ${escaparHTML(fechaPrincipal)}</p>
        <p>Edad: +18</p>
        <p>${escaparHTML(evento.tipo || "Evento")}</p>
        <button onclick="mostrar('mapa')">Comprar Boletas</button>
      </div>
    `);
  });
}

renderCarteleraPublicada();

window.addEventListener("storage", function(event) {
  if (["cartelera_usuario", "eventos_publicados", "eventos_base_eliminados"].includes(event.key)) {
    renderCarteleraPublicada();
  }
});

/* ========================
   ASIENTOS
   ======================== */

let seleccionados = [];

function crearAsientos(zona) {
  let letras = ["A", "B", "C", "D"];
  let cont   = document.getElementById(zona);

  for (let l of letras) {
    for (let i = 1; i <= 5; i++) {
      let a       = document.createElement("div");
      a.className = "asiento";
      a.innerText = l + i;

      a.onclick = function () {
        this.classList.toggle("seleccionado");

        if (this.classList.contains("seleccionado")) {
          seleccionados.push(this.innerText);
        } else {
          seleccionados = seleccionados.filter(x => x !== this.innerText);
        }
      };

      cont.appendChild(a);
    }
  }
}

crearAsientos("graderia1");
crearAsientos("graderia2");
crearAsientos("vip");

/* ========================
   PAGO
   ======================== */

function pagar() {
  if (seleccionados.length === 0) {
    alert("Seleccione asientos");
    return;
  }

  alert("Redirigiendo a PSE...");

  setTimeout(() => {
    alert("Compra realizada con éxito");

    document.getElementById("lista").innerHTML = "Asientos: " + seleccionados.join(", ");

    document.getElementById("qr").src =
      "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + seleccionados.join(",");

    mostrar("resultado");
  }, 1500);
}
