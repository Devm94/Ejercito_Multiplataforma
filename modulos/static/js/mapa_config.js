const capaOSM = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
});

const esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/' +
    'World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri',
    maxZoom: 20
});

const esriLabels = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/' +
    'Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Labels &copy; Esri',
    pane: 'overlayPane'
});

const map = L.map('map', {
    center: [14.664990, -86.895006],
    zoom: 7,
    fullscreenControl: true,
    fullscreenControlOptions: { position: 'topleft' },
    layers: [capaOSM]
});

const capasEstado = {
    'Abierto': L.layerGroup(),
    'Cerrado': L.layerGroup(),
    'Activo': L.layerGroup(),
    'Inactivo': L.layerGroup(),
    'Otro': L.layerGroup()
};

const rows = document.querySelectorAll("table tbody tr");
rows.forEach(row => {
    const lat = row.dataset.lat;
    const lng = row.dataset.lng;
    if (lat && lng) {
        const estado = row.cells[6].innerText.trim();
        let color;
        let capaDestino;
        switch (estado) {
            case 'Abierto': color = 'green'; capaDestino = capasEstado['Abierto']; break;
            case 'Cerrado': color = 'red'; capaDestino = capasEstado['Cerrado']; break;
            case 'Activo': color = 'orange'; capaDestino = capasEstado['Activo']; break;
            case 'Inactivo': color = 'gray'; capaDestino = capasEstado['Inactivo']; break;
            default: color = 'blue'; capaDestino = capasEstado['Otro'];
        }

        const marker = L.circleMarker([lat, lng], {
            radius: 3,
            color: color,
            fillColor: color,
            fillOpacity: 0.8
        }).bindPopup(`
  <div class="popup-table-container">
    <table class="popup-table">
        <h6 class="popup-title">${row.cells[5].innerText}</h6>
      <tr><th>Departamento</th><td>${row.cells[1].innerText}</td></tr>
      <tr><th>Municipio</th><td>${row.cells[2].innerText}</td></tr>
      <tr><th>Sector</th><td>${row.cells[3].innerText}</td></tr>
      <tr><th>Carga Electoral</th><td>${row.cells[4].innerText}</td></tr>
      <tr><th>Estado</th><td>${row.cells[6].innerText}</td></tr>
    </table>
    <div class="text-center">
      <button class="btn btn-sm btn-primary mt-2" onclick="verDetalle(${row.dataset.id})">
        Ver más
      </button>
    </div>
  </div>`
);

        marker.addTo(capaDestino);

        row.addEventListener('click', () => {
            map.setView(marker.getLatLng(), 20);
            marker.openPopup();
        });
    }
});

Object.values(capasEstado).forEach(capa => capa.addTo(map));

L.control.layers(
    {
        "OpenStreetMap": capaOSM,
        "Esri Satélite": L.layerGroup([esriSat, esriLabels])
    },
    {
        "Abierto": capasEstado['Abierto'],
        "Cerrado": capasEstado['Cerrado'],
        "Activo": capasEstado['Activo'],
        "Inactivo": capasEstado['Inactivo']
    },
    { collapsed: false }
).addTo(map); 