/* ========================
   NAVEGACIÓN ENTRE MÓDULOS
   ======================== */

function mostrar(id) {
  document.querySelectorAll(".modulo").forEach(m => m.classList.remove("active"));
  document.getElementById(id).classList.add("active");
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
