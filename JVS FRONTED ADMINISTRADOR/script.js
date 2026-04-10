// ===== DATOS DE PRODUCTOS =====
const productos = [
    { nombre: "Aguardiente Amarillo", cantidad: 10, precio: 25000, img: "imagen/aguardiente.G" },
    { nombre: "Cerveza Águila",        cantidad: 20, precio: 4000,  img: "aguila.WEBP" },
    { nombre: "Cerveza Corona",        cantidad: 15, precio: 6000,  img: "corona.WEBP" },
    { nombre: "Whisky",                cantidad: 8,  precio: 80000, img: "whisky.WEBP" }
];

// ===== LOGIN =====
function login() {
    const usuario   = document.getElementById("user").value;
    const contraseña = document.getElementById("pass").value;

    if (usuario === "admin" && contraseña === "1234") {
        document.getElementById("login").style.display = "none";
        document.getElementById("bienvenida").innerText = "Hola Admin, bienvenido";
    } else {
        alert("Datos incorrectos");
    }
}

// ===== FOTO DE PERFIL =====
function showOptions() {
    const opt = document.getElementById("photoOptions");
    opt.style.display = opt.style.display === "block" ? "none" : "block";
}

function changePhoto(src) {
    document.getElementById("mainPhoto").src = src;
}

// ===== MODAL COORDINADOR =====
function abrirCoord() {
    document.getElementById("ventanaCoord").style.display = "flex";
}

function cerrarCoord() {
    document.getElementById("ventanaCoord").style.display = "none";
}

// ===== MODAL VENDEDOR =====
function abrirVend() {
    document.getElementById("ventanaVend").style.display = "flex";
}

function cerrarVend() {
    document.getElementById("ventanaVend").style.display = "none";
}

// ===== MODAL SALARIO =====
function verSalario() {
    document.getElementById("ventanaSalario").style.display = "flex";
}

function cerrarSalario() {
    document.getElementById("ventanaSalario").style.display = "none";
}

// ===== INVENTARIO =====
function verInventarioVend() {
    document.getElementById("inventarioVend").style.display = "flex";
    renderInventario();
}

function cerrarInventario() {
    document.getElementById("inventarioVend").style.display = "none";
}

function renderInventario() {
    const contenedor = document.getElementById("listaInventario");
    contenedor.innerHTML = "";

    productos.forEach((p, i) => {
        contenedor.innerHTML += `
            <div class="producto-item">
                <div>
                    <b>${p.nombre}</b><br><br>
                    Cantidad: ${p.cantidad}
                    <div style="margin-top:5px;">
                        <button onclick="sumar(${i})">+</button>
                        <button onclick="restar(${i})">-</button>
                        <button onclick="eliminarProducto(${i})" style="background:#7a0018;border:none;">Eliminar</button>
                    </div>
                    Precio: $${p.precio.toLocaleString("es-CO")}
                </div>
                <img src="${p.img}" class="inventario-img">
            </div>
        `;
    });
}

function sumar(i) {
    productos[i].cantidad++;
    renderInventario();
}

function restar(i) {
    if (productos[i].cantidad > 0) {
        productos[i].cantidad--;
        renderInventario();
    }
}

function eliminarProducto(i) {
    if (confirm("¿Seguro que quieres eliminar este producto?")) {
        productos.splice(i, 1);
        renderInventario();
    }
}

function agregarProducto() {
    const nombre   = prompt("Nombre del producto:");
    const cantidad = prompt("Cantidad:");
    const precio   = prompt("Precio:");

    if (nombre && cantidad && precio) {
        productos.push({
            nombre:   nombre,
            cantidad: parseInt(cantidad),
            precio:   parseInt(precio),
            img:      "default.jpg"
        });
        renderInventario();
    }
}

function guardarCambios() {
    alert("Cambios guardados correctamente");
}

// ===== OTRAS FUNCIONES =====
function verInventario() {
    window.location.href = "raider.html";
}

function verProveedores() {
    alert("Aquí se mostrarán los proveedores");
}
