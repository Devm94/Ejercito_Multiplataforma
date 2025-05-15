  var map = L.map('map').setView([14.664990, -86.895006], 7);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  var marker;
  function addMarker(lat, lng) {
      if (marker) {map.removeLayer(marker); }
      marker = L.marker([lat, lng]).addTo(map);
      document.getElementById('latitude').value = lat;
      document.getElementById('longitude').value = lng;
  }
  map.on('click', function (e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    addMarker(lat, lng);});
    function goToMyLocation() {
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function (position) {
              var lat = position.coords.latitude;
              var lng = position.coords.longitude;
              // Centrar el mapa y agregar el marcador
              map.setView([lat, lng], 13);
              addMarker(lat, lng);
          }, function () {
              alert('No se pudo obtener la ubicación.');
          });
      } else {
          alert('La geolocalización no está soportada en este navegador.');
      }
  }
  var goToMyLocationButton = L.control({position: 'topright'});
  goToMyLocationButton.onAdd = function(map) {
      var button = L.DomUtil.create('a', 'leaflet-bar');
      button.href = '#';
      button.innerHTML = '<i class="fas fa-location-arrow"></i>'; // Icono del marcador
      button.title = 'Ir a mi ubicación';
      button.style.fontSize = '20px'
      button.onclick = function() {
          goToMyLocation();
      };
      return button;
  };
  goToMyLocationButton.addTo(map);
  const dropZone = document.querySelector('.drop-zone');
  const fileInput = document.getElementById('imageInput');
  const previewImage = document.getElementById('previewImage');
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      handleFile(fileInput.files[0]);
    }
  });
  dropZone.addEventListener('click', () => {
    fileInput.click();
  });
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
      handleFile(fileInput.files[0]);
    }
  });
  function handleFile(file) {
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = () => {
        previewImage.src = reader.result;
        previewImage.classList.remove('d-none');
      };
      reader.readAsDataURL(file);
    } else {
      alert('Por favor, selecciona un archivo de imagen válido.');
    }
  }