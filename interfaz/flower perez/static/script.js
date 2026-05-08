let myChart = null;

// --- NAVEGACIÓN ---
function showSection(id) {
    document.getElementById('welcome-msg').classList.add('hidden');
    document.getElementById('tool-container').classList.remove('hidden');
    document.querySelectorAll('.form-content').forEach(f => f.classList.add('hidden'));
    document.getElementById(id).classList.remove('hidden');

    if (id === 'sec-dashboard') initChart();
    if (id === 'sec-venta') cargarCombosVenta();
}

// --- LOGIN ---
async function login() {
    const user = document.getElementById('l-user').value;
    const pwd = document.getElementById('l-pwd').value;
    const res = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ user, pwd })
    });
    if (res.ok) {
        document.getElementById('login-screen').classList.add('hidden');
        document.getElementById('main-app').classList.remove('hidden');
        showSection('sec-dashboard');
    } else alert("Acceso denegado");
}

// --- GUARDAR DATOS ---
async function guardarFlor() {
    const data = {
        nombre: document.getElementById('f-nombre').value,
        tipo: document.getElementById('f-tipo').value,
        variedad: document.getElementById('f-variedad').value,
        cantidad: document.getElementById('f-cant').value
    };
    if (!data.nombre || !data.cantidad) return alert("Complete los campos");
    await enviarAlServidor('flores', data, ['f-nombre', 'f-tipo', 'f-variedad', 'f-cant']);
}

async function enviarVenta() {
    const data = {
        cliente_id: document.getElementById('v-id-cli').value,
        flor_id: document.getElementById('v-id-flo').value,
        cantidad: document.getElementById('v-cant').value,
        total: document.getElementById('v-total').value
    };
    if (!data.cliente_id || !data.flor_id) return alert("Seleccione cliente y flor");
    const res = await fetch('/guardar/ventas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if (res.ok) {
        alert("✨ Venta Exitosa");
        cargarCombosVenta();
    } else {
        const err = await res.json();
        alert("Error: " + err.message);
    }
}

async function enviarFormGenerico(ruta, camposMap) {
    let data = {};
    let IDs = [];
    for (let key in camposMap) {
        data[key] = document.getElementById(camposMap[key]).value;
        IDs.push(camposMap[key]);
        if (!data[key]) return alert("Complete todos los campos");
    }
    await enviarAlServidor(ruta, data, IDs);
}

async function enviarAlServidor(ruta, data, inputs) {
    const res = await fetch(`/guardar/${ruta}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if (res.ok) {
        alert("✨ Guardado correctamente");
        inputs.forEach(id => document.getElementById(id).value = "");
    }
}

// --- REPORTES ---
async function cargarReporte(categoria) {
    showSection('sec-reporte');
    const res = await fetch(`/reporte/${categoria}`);
    const datos = await res.json();
    const head = document.getElementById('tabla-head');
    const body = document.getElementById('tabla-body');
    document.getElementById('repo-titulo').innerText = "REPORTES: " + categoria.toUpperCase();

    if (datos.length > 0) {
        const columnas = Object.keys(datos[0]);
        // Encabezados dinámicos
        head.innerHTML = `<tr>${columnas.map(c => `<th>${c.toUpperCase()}</th>`).join('')} <th>ACCIONES</th></tr>`;
        
        body.innerHTML = datos.map(fila => `
            <tr>
                ${columnas.map(col => `<td>${fila[col]}</td>`).join('')}
                <td>
                    <button class="btn-delete" onclick="eliminar('${categoria}', ${fila.id || fila.ID})">
                        Borrar
                    </button>
                </td>
            </tr>
        `).join('');
    } else {
        body.innerHTML = "<tr><td colspan='10'>Sin registros.</td></tr>";
    }
}

async function eliminar(cat, id) {
    if (confirm("¿Seguro de eliminar este registro?")) {
        await fetch(`/eliminar/${cat}/${id}`, { method: 'DELETE' });
        cargarReporte(cat);
    }
}

function filtrarTablaReporte() {
    const val = document.getElementById('repo-search').value.toUpperCase();
    const filas = document.querySelectorAll('#tabla-body tr');
    filas.forEach(f => f.style.display = f.innerText.toUpperCase().includes(val) ? '' : 'none');
}

async function cargarCombosVenta() {
    const [resC, resF] = await Promise.all([fetch('/reporte/clientes'), fetch('/reporte/flores')]);
    const clientes = await resC.json();
    const flores = await resF.json();
    const selC = document.getElementById('v-id-cli');
    const selF = document.getElementById('v-id-flo');
    selC.innerHTML = '<option value="">-- Seleccionar Cliente --</option>';
    clientes.forEach(c => selC.innerHTML += `<option value="${c.id}">${c.nombre}</option>`);
    selF.innerHTML = '<option value="">-- Seleccionar Flor --</option>';
    flores.forEach(f => {
        if(f.cantidad > 0) selF.innerHTML += `<option value="${f.id}">${f.nombre} (Stock: ${f.cantidad})</option>`;
    });
}

async function initChart() {
    const res = await fetch('/reporte/ventas');
    const ventas = await res.json();
    const agrupar = {};
    ventas.forEach(v => {
        const fechaRaw = v.FECHA || v.fecha;
        const f = new Date(fechaRaw).toLocaleDateString();
        const totalRaw = v.TOTAL || v.total;
        agrupar[f] = (agrupar[f] || 0) + parseFloat(totalRaw);
    });
    const ctx = document.getElementById('ventasChart').getContext('2d');
    if (myChart) myChart.destroy();
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(agrupar),
            datasets: [{ label: 'Ventas Diarias $', data: Object.values(agrupar), borderColor: '#27ae60', fill: false }]
        }
    });
}