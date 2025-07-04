function mostrarCentros(cod_municipio) {
fetch(`/centros_municipio/${cod_municipio}`)
    .then(res => res.json())
    .then(data => {
        const contenedor = document.getElementById('listaCentros');
        contenedor.innerHTML = '';
        if (data.length === 0) {
            contenedor.innerHTML = '<p>No hay centros registrados.</p>';
        } else {
            const tabla = document.createElement('table');
            tabla.classList.add('table', 'table-striped', 'table-bordered');
            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th>No.</th>
                    <th>Nombre del Centro</th>
                    <th>Estado</th>
                    <th>Contactos</th>
                </tr>`;
            tabla.appendChild(thead);

            // Crear cuerpo de la tabla
            const tbody = document.createElement('tbody');
            data.forEach((centro, index) => {
                const fila = document.createElement('tr');
                fila.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${centro.nombre}</td>
                    <td>${centro.estado}</td>
                    <td>            <button class="btn btn-sm btn-info" onclick="abrirCollapse('${index}', this)">
                Ver contactos
            </button>
            <button class="btn btn-sm btn-danger d-none" onclick="cerrarCollapse('${index}', this)">
                Cerrar contactos
            </button></td>
                `;
                tbody.appendChild(fila);
                const filaDetalles = document.createElement('tr');
                    filaDetalles.innerHTML = `
                        <td colspan="4" class="p-0 border-0">
                            <div id="${index}" class="collapse p-2">    
                            ${generarTablaContacto(centro.contactos)}
                            </div>
                        </td>
                    `;
                    tbody.appendChild(filaDetalles);
            });

            tabla.appendChild(tbody);
            contenedor.appendChild(tabla);
        }

        // Mostrar modal (requiere Bootstrap y jQuery)
        $('#modalCentros').modal('show');
    })
    .catch(err => {
        alert("No se pudieron cargar los centros.");
        console.error(err);
    });
  }

function abrirCollapse(id, botonVer) {
    const collapseElement = document.getElementById(id);
    const bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: true });

    // Mostrar el botón de cerrar
    const botonCerrar = botonVer.nextElementSibling;
    botonCerrar.classList.remove('d-none');
    botonVer.classList.add('d-none');
}
function cerrarCollapse(id, botonCerrar) {
    const collapseElement = document.getElementById(id);
    const bsCollapse = new bootstrap.Collapse(collapseElement, { toggle: false });
    bsCollapse.hide();

    // Mostrar el botón de ver nuevamente
    const botonVer = botonCerrar.previousElementSibling;
    botonVer.classList.remove('d-none');
    botonCerrar.classList.add('d-none');
}

function generarTablaContacto(contactos) {
    if (!contactos || contactos.length === 0) {
        return '<p class="text-muted">No hay contactos disponibles.</p>';
    }

    let html = `
        <table class="table table-sm table-bordered mb-0">
            <thead>
                <tr>
                    <th>Nombre</th>
                    <th>Teléfono</th>
                    <th>Foto</th>
                </tr>
            </thead>
            <tbody>
    `;

    contactos.forEach(contacto => {
        html += `
            <tr>
                <td>${contacto.nombre}</td>
                <td>${contacto.numero}</td>
                                <td>
                    ${contacto.imagen ? `<img src="${contacto.imagen}" alt="Foto" width="50">` : 'Sin imagen'}
                </td>
            </tr>
        `;
    });

    html += `</tbody></table>`;
    return html;
}
